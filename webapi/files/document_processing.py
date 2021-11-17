# %%
from docx import Document
import re
from difflib import SequenceMatcher
from models.model import *

# %%
def process_report(filename):
    """
    Process report for data extraction

    param filename: filename to open and extract data from
    """
    return read_document(Document(open(filename, 'rb')))

def read_document(document):
    """
    Read in document and extract all data from it.
    :param document: opened document from python-docx.
    """
    report = get_report_info(document)
    
    slos = []
    measures = [[]]
    analysisList = [[]]
    decisions = []
    for table in get_table_cells(document):
        # Empty table
        if len(table) < 1: 
            continue
        # SLO data
        if SequenceMatcher(None, table[0]['cell'], "Student Learning Outcomes").ratio() >= 0.9:
            slos = get_slo_data(table)
        # Assessmment data
        elif re.match(re.compile('SLO..:'), table[0]['cell']):
            # measures.append(get_measures_data(table))
            #TODO figure out how to make this work in a method call
            sloNum = ""
            state = ""
            measure = Measure().to_dict()
            for cell in table:
                if state != "":
                    measure = state_match(state, measure, cell)
                    state = ""
                    continue
                # if we have a new SLO num, add it to the list and move to the next
                # Note: there may be multiple measures for one SLO, need to preserve number
                if re.match(re.compile('^SLO..:'), cell['cell']):
                    num = extract_text(cell['cell'], "SLO ")[0]
                    if sloNum != "":
                        idx = int(sloNum)
                        while len(measures) < idx:
                            measures.append([]) 
                        measures[idx-1].append(measure)
                        measure = Measure().to_dict()
                    sloNum = num
                    measure['slo_id'] = sloNum
                    continue
                if "Title" in cell['cell']:
                    measure['title'] = extract_text(cell['cell'], ":").lstrip()
                    continue
                if "Measure Aligns to the SLO" in cell['cell']:
                    measure['description'] = extract_text(cell['cell'], "SLO").lstrip()
                    continue
                for st in ["Domain", "Type", "Point in Program", "Population", "Frequency", "Threshold", "Program"]:
                    if st in cell['cell']:
                        state = map_state(st)
                        break
            idx = int(sloNum)
            while len(measures) < idx:
                measures.append([]) 
            measures[idx-1].append(measure)
        # Analysis Data
        elif is_analysis(table):
            analysisList = get_analysis_data(table)
        # Decisions/Actions Data
        elif re.match(re.compile('^SLO..'), table[0]['cell']) and not status_table(table):
            decisions = get_decisions_data(table)
        else:
            print("TODO or Misc data found")
    
    return [report, slos, measures, analysisList, decisions]

#TODO clean up, possibly make a process_engine class with below methods to leave this file cleaner

def get_measures_data(table):
    measures = []
    for cell in table:
        print(cell)
    return measures

def get_analysis_data(table):
    sloNum = ""
    analysisList = [[]]
    analysis = CollectionAnalysis()
    for cell in table:
        # if we have a new SLO num, add it to the list and move to the next
        # Note: there may be multiple analysis for one SLO, need to preserve number
        if "SLO " in cell['cell']:
            for c in cell['cell']:
                if c.isdigit():
                    num = c
                    break
            if sloNum != "":
                idx = int(sloNum)
                while len(analysisList) < idx:
                    analysisList.append([])
                analysisList[idx-1].append(analysis)
                analysis = CollectionAnalysis()
            sloNum = num
        elif "%" in cell['cell']:
            analysis.percentage_who_met_or_exceeded = cell['cell']
        elif is_year(cell['cell']):
            analysis.data_collection_date_range = cell['cell']
        elif not re.match(re.compile('^Note:'), cell['cell']):
            analysis.number_of_students_assessed = cell['cell']
    idx = int(sloNum)
    while len(analysisList) < idx:
        analysisList.append([])
    analysisList[idx-1].append(analysis)
    return analysisList

def get_decisions_data(table):
    sloNum = ""
    decisions = []
    decision = DecisionsAction
    for cell in table:
        # if we have a new SLO num, add it to the list and move to the next
        if re.match(re.compile('^SLO..$'), cell['cell']):
            num = cell['cell'].split("SLO ")[1]
            if sloNum != "":
                decisions.append(decision)
                decision = DecisionsAction()
            sloNum = num
        else:
            decision.content = cell['cell']
    decisions.append(decision)
    return decisions

def status_table(table):
    for cell in table:
        if "Partially Met" in cell['cell']:
            return True
    return False
 
def is_year(text):
    year = ""
    found = False
    for c in text:
        if c.isdigit():
            year += c
            found = True
        elif found:
            break
    if year != "":
        return int(year) > 1900
    return False

def is_analysis(table):
    for cell in table:
        if SequenceMatcher(None, cell['cell'], "Data Collection Date Range").ratio() >= 0.95:
            return True
    return False

def get_slo_data(table):
    slos = []
    slo = SLO()
    for cells in table:
        slo = slo_matcher(cells['cell'], slo)
        if(slo.description != ""):
            if not has_duplicate(slos, slo):
                slos.append(slo)
            slo = SLO()
        if not cells['checkboxes']:
            text = cells['cell']
            for c in text:
                if isinstance(c, str) and is_checkbox(c):
                    parts = text.split(chr(9746))  
                    if len(parts) > 1:
                        for p in parts:
                            result = get_first_word(p).strip()
                            slos = slo_attr_match(result, slos)
                    break
        elif cells['checkboxes']:
            pos = 0
            for cb in cells['checkboxes']:
                for child in cb.getchildren():
                    if child.tag.endswith("checked"):
                        if(int(re.search(r'\d+', child.values()[0]).group())):
                            word = get_word_at(pos, cells['cell'])
                            slos = slo_attr_match(word, slos)
                        pos += 1
    return slos

# TODO eventually instead of saving all data in a list(memory heavyish), just extract data here?
def get_table_cells(document):
    tableCells = [[]]
    for table in document.tables:
        cell_information = []
        for row in table.rows:
            # cells get duplicated if they are merged cells
            for cell in iter_unique_cells(row):
                p = cell._element
                checkboxes = p.xpath('.//w14:checkbox')
                val = {"cell":  cell.text.strip(), "checkboxes": checkboxes}
                cell_information.append(val)
        tableCells.append(cell_information)
    return tableCells

def get_report_info(document):
    report = Report()
    for paragraph in document.paragraphs:
        if paragraph.text == '':
            continue
        if report.title == "":
            report.title = paragraph.text
        report = report_matcher(paragraph.text, report)
        if is_full(report): #early exit for faster time but can be removed
            return report
    return report
    
def map_state(st):
    """
    maps a state to a Measure attribute, this makes 
    setting an attribute with a dict very easy

    param st: st to map
    """
    if st == "Domain":
        return "domain"
    if st == "Type":
        return "type"
    if st == "Point in Program":
        return "point_in_program"
    if st == "Population":
        return "population_measured"
    if st == "Frequency":
        return "frequency_of_collection"
    if st == "Threshold":
        return "proficiency_threshold"
    if st == "Program":
        return "proficiency_target"

def state_match(state, m, cell):
    """
    Given a state, find the necessary data in the cell
    and then set that in the measure object

    param state: state used to set attribute of Measure
    param m: Measure to update
    param cell: cell data to look through
    """
    if state == "proficiency_threshold" or state == "proficiency_target":
        if cell['cell'] != "Describe:":
            m[state] = cell['cell']
        return m
    checked = []
    if cell['checkboxes']:
        pos = 0
        for cb in cell['checkboxes']:
            for child in cb.getchildren():
                if child.tag.endswith("checked"):
                    if(int(re.search(r'\d+', child.values()[0]).group())):
                        words = re.findall('[a-zA-Z][^A-Z]*', cell['cell'])
                        if "Sample of students" in words[pos]:
                            idx = 0
                            text = ""
                            for items in words:
                                if idx >= pos:
                                    text += words[idx]
                                idx += 1
                            checked.append(text.lstrip())
                        elif "Direct" in words[pos]:
                            checked.append(words[pos] + " " + words[pos+1])
                        else:
                            checked.append(words[pos].lstrip())
                    pos += 1
    else:
        text = cell['cell']
        items = text.split(chr(9746))
        items.pop(0)
        for text in items:
            checked.append(text.split(chr(9744))[0].lstrip())
    if len(checked) > 0:
        m[state] = ', '.join(checked)
    return m

def iter_unique_cells(row):
    """
    Generate cells in `row` skipping empty grid cells.
    Without this, there will be duplicate cells in table cells

    param row: row to have dupes removed
    """
    prior_tc = None
    for cell in row.cells:
        this_tc = cell._tc
        if this_tc is prior_tc:
            continue
        prior_tc = this_tc
        yield cell

def get_word_at(pos, text):
    """
    Breaks up the sentence into individual words 
    and gives the word at the specified position

    param text: text to break up
    param pos: position to get the word at
    """
    words = []
    inword = 0
    for c in text:
        if c in " \r\n\t":
            inword = 0
        elif not inword:
            words = words + [c]
            inword = 1
        else:
            words[-1] = words[-1] + c
    return words[pos]

def slo_attr_match(word, slos):
    """
    Match a word to an slo attribute for setting data

    param word: word to match to slo attribue
    param slo: slo to set data into
    """
    # rework this as taxonomy levels may not be all of these
    if(word in ["Knowledge", "Analysis", "Comprehension","Synthesis","Application", "Evaluation"]):
        for slo in slos:
            if slo.bloom == "":
                slo.bloom = word
                break
    elif(word in ["1", "2", "3", "4", "Not applicable for SLO"]):
        for slo in slos:
            if slo.common_graduate_program_slo == "":
                slo.common_graduate_program_slo = word
                break
    return slos

def get_first_word(str):
    """
    Returns the first word in a string

    param str: string to retrieve word from
    """
    result = ""
    special_chars = "/ \\@!&*().?,"
    for c in str:
        if is_checkbox(c):
            return result
        elif c.isalpha() or c in special_chars:
            result += c
    return result

def is_checkbox(c):
    """
    checks if given character is a ascii checkbox
 
    param c: char to check
    """
    number = ord(c)
    return not c.isalpha() and number == 9744 or number == 9746

def has_duplicate(slos, slo):
    """
    Take a list of slos and determine if it already has the same slo in it

    :param slos: list of slos.
    :param slo: slo to be checked against.
    """
    for sloItem in slos: 
        if SequenceMatcher(None, sloItem.description, slo.description).ratio() >= 0.8:
            return True    
    return False

def is_full(report):
    """
    checks if report data is filled to exit early
 
    param report: report to check
    """
    return (report.college != "" and report.department != "" 
            and report.program != "" and report.degree_level != "" 
            and report.academic_year != "" and report.date_range != "" 
            and report.author != "")

def report_matcher(str, report:Report):
    """
    Reads a string to extract the main report data

    :param str: string to look at for data.
    :param report: report object that will be updated and returned.
    """
    if report is None:
        report = Report()
    if "College:" in str:
        report.college = extract_text(str, "College:")
    if "Department/School:" in str:
        report.department = extract_text(str, "Department/School:")
    if "Program:" in str:
        report.program = extract_text(str, "Program:")
    if "Degree Level:" in str:
        report.degree_level = extract_text(str, "Degree Level:")
    if "Academic Year of Report:" in str:
        report.academic_year = extract_text(str, "Academic Year of Report:")
    if "Date Range of Reported Data:" in str:
        report.date_range = extract_text(str, "Date Range of Reported Data:")
    if "Person Preparing the Report:" in str:
        report.author = extract_text(str, "Person Preparing the Report:")
    return report

def slo_matcher(str, slo:SLO):
    """
    Reads a string to extract the main slo data

    :param str: string to look at for data.
    :param slo: slo object that will be updated and returned.
    """
    if slo is None:
        slo = SLO()
    regex = re.compile('^SLO..:')
    if re.match(regex, str):
        for text in re.split(":", str):
            if "SLO" in text:
                slo.id = text
            elif(text != ""):
                slo.description = text.strip()
    return slo

def extract_text(str, split_point):
    """
    Reads a string to split text and remove tab characters.
    Some text separate information with tabs so we only want the beginning
    ex:
        College:\\t<text>\\t\\t\\t <other text>
    we want just <text> so split at College: and \\t

    :param str: string to be split.
    :param split_point: string match to split at.
    """
    pieces = str.split(split_point)
    if(len(pieces) < 2):
        return ""
    sections = pieces[1].split("\t")
    for parts in sections:
        toReturn = parts.lstrip() 
        if toReturn != '':
            return toReturn
    return ""    