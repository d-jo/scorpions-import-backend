# %%
from docx import Document
import xml.etree.ElementTree as ET
import pandas as pd
from docx.oxml.ns import qn

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
    if tr.tag.endswith("t"):
        result.append((tr.text.strip()))
        pass
    if tr.tag.endswith("checked"):
        for attr in tr.attrib:
            if attr.endswith("val"):
                checked = tr.attrib[attr]
                # Only add the ones that are checked, other are assumed not checked by default
                if checked == '1':
                    result.append(("checkbox", checked))
                
    #if tr.tag.endswith()
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
        dxml = p.xml
        with open("./test2.xml", 'w') as f:
            f.write(dxml)
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

    #for a in cell_information:
    #    if not a['checkboxes']:
    #        continue
    #    print(a['cell'].paragraphs[0].text)
    #    if a['checkboxes']:
    #        #print(a['checkboxes'])
    #        for cb in a['checkboxes']:
    #            for child in cb.getchildren():
    #                if child.tag.endswith("checked"):
    #                    print("\t" + child.values()[0])
    #    print("==========")

    # pandas_table(document)




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
                cell_information.append({"cell":  cell, "checkboxes": checkboxes})
                #for para in cell.paragraphs:
                #    if checkboxes:
                #        print(checkboxes)
                #    if para.text == '':
                #        continue

                    #tableParas.append(para)
                    #tablesCellsText.append(para.text.strip())
    #print('Document plain text\n')
    #print('****************************************************\n')
    ##print('\n==========\n'.join(documentText))
    #print('****************************************************\n')


    #print('Document table text\n')
    #print('****************************************************\n')
    #print('\n==========\n'.join(tablesCellsText))
    #print('****************************************************\n')
    
    #is_checked(rows)
    #is_checked(tableParas)
    #print(cell_information)
    for a in cell_information:
        if not a['checkboxes']:
            continue
        print(a['cell'].paragraphs[0].text)
        if a['checkboxes']:
            #print(a['checkboxes'])
            for cb in a['checkboxes']:
                for child in cb.getchildren():
                    if child.tag.endswith("checked"):
                        print("\t" + child.values()[0])
        print("==========")

    # pandas_table(document)


f = open('../../old/data/grad2018-regular.docx', 'rb')
document = Document(f)
#doc_elm = document._element
#with open("./test22.xml") as f:

#cbs = doc_elm.xpath('w:p')
#print(cbs)
r = read_document2(document)
# %%

# w:tc
#   w:p
#       w:sdt -> w:sdtPr
#           w14:checkbox -> w14:checked
#       w:r
#           w:t = text
#           
#      