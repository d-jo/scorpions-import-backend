# %%
from docx import Document
from docx.oxml.ns import qn
from lxml import etree


def is_checked(docElements):
    """Not able to detemine if checkbox is checked or not."""
    for docElem in docElements:
        checkboxes = etree.ElementBase.xpath(docElem._element, './/w14:checkbox', namespaces=docElem._element.nsmap)
        for checkbox in checkboxes:
            p = docElem._element
            print(checkbox)
            print(p.xml)
            for item in checkbox.findall('.//w14:checkbox', namespaces=docElem._element.nsmap):
                print(item)
                print(etree.dump(item))


def read_document(document):
    """Read in document and print out the paragraph contents."""
    documentText = []
    documentElements = []
    for paragraph in document.paragraphs:
        if paragraph.text == '':
            continue
        documentText.append(paragraph.text)
        documentElements.append(paragraph)
        print(paragraph)
    print('\n'.join(documentText))
    # is_checked(documentElements)


f = open('./data/grad2018-regular.docx', 'rb')
document = Document(f)
read_document(document)
# %%

# w:tc
#   w:p
#       w:sdt -> w:sdtPr
#           w14:checkbox -> w14:checked
#       w:r
#           w:t = text
#           
#      

# %%

import xml.etree.ElementTree as ET


tree=ET.parse('data/test/word/document.xml')

def rec_traverse(tr):
    result = []
    if tr.tag.endswith("t"):
        result.append((tr.tag, tr.text))
        pass
    if tr.tag.endswith("checked"):
        for attr in tr.attrib:
            if attr.endswith("val"):
                checked = tr.attrib[attr]
                result.append(("checkbox", checked))
                
    #if tr.tag.endswith()
    for c in tr:
        result.extend(rec_traverse(c))
    
    return result
# %%
