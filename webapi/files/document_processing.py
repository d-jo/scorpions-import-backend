# %%
from docx import Document
import xml.etree.ElementTree as ET
import pandas as pd
from docx.oxml.ns import qn
from report import *
import re
from difflib import SequenceMatcher

def pandas_table(document, table_num=1, nheader=1):
    """
    Attempt at printing tables in a easy-to-read format
    https://medium.com/@karthikeyan.eaganathan/read-tables-from-docx-file-to-pandas-dataframes-f7e409401370
    :param document: opened document from python-docx.
    :param table_num: table number in document.
    :param nheader: number of headers in table.
    """
    table = document.tables[table_num-1]
    data = [[cell.text for cell in row.cells] for row in table.rows]
    df = pd.DataFrame(data)
    if nheader == 1:
        df = df.rename(columns=df.iloc[0]).drop(df.index[0]).reset_index(drop=True)
    elif nheader == 2:
        outside_col, inside_col = df.iloc[0], df.iloc[1]
        hier_index = pd.MultiIndex.from_tuples(list(zip(outside_col, inside_col)))
        df = pd.DataFrame(data, columns=hier_index).drop(df.index[[0,1]]).reset_index(drop=True)
    elif nheader > 2:
        print("more than two headers not supported")
        df = pd.DataFrame()
    print(df)


def rec_traverse(tr):
    """
    Recusively go through xml tags to find checkboxes and their value.
    :param tr: tag element.
    """
    result = []
    if tr.tag.endswith("t") and not tr.text is None:
        result.append((tr.text.lstrip()))
        pass
    if tr.tag.endswith("checked"):
        for attr in tr.attrib:
            if attr.endswith("val"):
                checked = tr.attrib[attr]
                print(attr + " : " + checked)
                # Only add the ones that are checked, other are assumed not checked by default
                if checked == '1':
                    result.append(("checkbox", checked))
                
    for c in tr:
        result.extend(rec_traverse(c))
    
    return result


def is_checked(docElements):
    """
    Going through paragraph elements, determine if contents
    has a checkbox, and if it is checked or not.
    :param docElements: array of paragraph elements from python-docx.
    """
    for docElem in docElements:
        # checkboxes = etree.ElementBase.xpath(docElem._element, './/w14:checkbox', namespaces=docElem._element.nsmap)
        p = docElem._element
        # dxml = p.xml
        # with open("./test2.xml", 'w') as f:
        #     f.write(dxml)
        tree=ET.fromstring(p.xml)
        for a in rec_traverse(tree):
            print(a)


def read_document2(document):
    """
    Read in document and parse the tables and checkboxes inside of them

    the returned object is an array of the form:
    [
        
        [ #table1
            [cell1, cell2],
            [cell3, cell4]
        ], 
        [ #table2
            [cell1, cell2],
            [cell3, cell4]
        ] ...
    ]

    :param document: opened document from python-docx.
    """

    curr_table = 0
    tables = []

    for table in document.tables:
        tables.append([])

        curr_row = 0

        for row in table.rows:
            tables[curr_table].append([])
            curr_cell = 0

            for cell in row.cells:
                p = cell._element
                checkboxes = p.xpath('.//w14:checkbox')
                print(checkboxes)
                obj = {
                    "cell_obj": cell, 
                    "table": curr_table, 
                    "row": curr_row, 
                    "cell": curr_cell
                    }
                if checkboxes is not None:
                    obj["checkboxes"] = checkboxes

                tables[curr_table][curr_row].append(obj)

                curr_cell += 1
            
            curr_row += 1
        
        curr_table += 1

    return tables

def read_document(document):
    """
    Read in document and print out the paragraph contents.
    :param document: opened document from python-docx.
    """
    documentText = []
    documentElements = []
    for paragraph in document.paragraphs:
        if paragraph.text == '':
            continue
        documentText.append(paragraph.text)
        documentElements.append(paragraph)
    tableParas = []
    tablesCellsText = []
    cell_information = []
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                p = cell._element
                checkboxes = p.xpath('.//w14:checkbox')
                cell_information.append({"cell":  cell.text, "checkboxes": checkboxes})
                for para in cell.paragraphs:
                   if para.text == '':
                       continue
                   tableParas.append(para)
                   tablesCellsText.append(para.text.strip())
    #print('Document plain text\n')
    #print('****************************************************\n')
    # print('\n==========\n'.join(documentText))
    report = Report()
    slo = SLO()
    for text in documentText:
        report = report_matcher(text, report)
        if is_full(report):
            break
    for text in tablesCellsText:
        slo = slo_matcher(text, slo)
        if(slo.title != ""):
            if not has_duplicate(report.slos, slo):
                report.slos.append(slo)
            slo = SLO()

    #print('****************************************************\n')


    #print('Document table text\n')
    #print('****************************************************\n')
    # print('\n==========\n'.join(tablesCellsText))
    #print('****************************************************\n')
    
    for a in cell_information:
        if not a['checkboxes']:
            text = a['cell']
            for c in text:
                if isinstance(c, str) and is_checkbox(c):
                    parts = text.split(chr(9746))  
                    if len(parts) > 1:
                        report = get_blooms_tax_level(parts, report)
                    break
        elif a['checkboxes']:
            # print(a['cell'])
            pos = 0
            for cb in a['checkboxes']:
                for child in cb.getchildren():
                    if child.tag.endswith("checked"):
                        if(int(re.search(r'\d+', child.values()[0]).group())):
                            word = get_word_at(pos, a['cell'])
                            if(word in SLO.BLOOMSTAX):
                                for slo in report.slos:
                                    if slo.bloomsTaxonomyLevel == "":
                                        slo.bloomsTaxonomyLevel = word
                                        break
                            if(word in SLO.COMMONGRAD):
                                for slo in report.slos:
                                    if slo.commonGraduateSlos == "":
                                        slo.commonGraduateSlos = word
                                        break
                        pos += 1
    
    return report

#TODO clean up, possibly make a process_engine class with below methods to leave this file cleaner

def get_word_at(pos, text):
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
    
def get_blooms_tax_level(parts, report):
    for p in parts:
        result = get_first_word(p).strip()
        if(result in SLO.BLOOMSTAX):
            for slo in report.slos:
                if slo.bloomsTaxonomyLevel == "":
                    slo.bloomsTaxonomyLevel = result
                    break
    return report

def get_first_word(str):
    result = ""
    special_chars = "/ \\@!&*().?,"
    for c in str:
        if is_checkbox(c):
            return result
        elif c.isalpha() or c in special_chars:
            result += c
    return result

def is_checkbox(c):
    number = ord(c)
    return not c.isalpha() and number == 9744 or number == 9746

def has_duplicate(slos, slo):
    """
    Take a list of slos and determine if it already has the same slo in it

    :param slos: list of slos.
    :param slo: slo to be checked against.
    """
    for sloItem in slos: 
        if SequenceMatcher(None, sloItem.title, slo.title).ratio() >= 0.8:
            return True    
    return False

def is_full(report):
    return (report.college != "" and report.department != "" 
            and report.program != "" and report.degreeLevel != "" 
            and report.academicYear != "" and report.dateRange != "" 
            and report.personPreparing != "")
#%%
def process():
    f = open('../../old/data/undergrad2018-regular.docx', 'rb')
    document = Document(f)
    return read_document(document)
# %%

def process_report(filename):
    return read_document(Document(open(filename)))

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
        report.degreeLevel = extract_text(str, "Degree Level:")
    if "Academic Year of Report:" in str:
        report.academicYear = extract_text(str, "Academic Year of Report:")
    if "Date Range of Reported Data:" in str:
        report.dateRange = extract_text(str, "Date Range of Reported Data:")
    if "Person Preparing the Report:" in str:
        report.personPreparing = extract_text(str, "Person Preparing the Report:")
    return report

def slo_matcher(str, slo:SLO):
    """
    Reads a string to extract the main slo data

    :param str: string to look at for data.
    :param slo: slo object that will be updated and returned.
    """
    if slo is None:
        slo = SLO()
    regex = re.compile('^SLO..: \w')
    if re.match(regex, str):
        for text in re.split("^SLO..: ", str): 
            if(text != ""):
                slo.title = text
                break
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
    sections = str.split(split_point)[1].split("\t")
    for parts in sections:
        toReturn = parts.lstrip() 
        if toReturn != '':
            return toReturn
    return ""    