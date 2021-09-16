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


f = open('./data/test-checkbox.docx', 'rb')
document = Document(f)
read_document(document)