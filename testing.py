# %%

from docx import Document


# %%

#f = open('./data/grad2018-regular.docx', 'rb')
f = '/home/djo/Documents/UNOMAHA/Fall2021/CSCI4970Capstone/scorpions-academic-import/backend/data/test/word/document.xml'

import xml.etree.ElementTree as ET
tree = ET.parse(f)
root = tree.getroot()

for child in root:
  for c2 in child:
    print(c2.tag, c2.text)
#document = Document(f)

# %%

#for p in document.tables:
  #for i in range(0, len(p.columns)):
    #c = p.cell(0, i).text
    #print(c)
    #print(type(c))
  #print('\n')


# %%

#t = document.tables[5]
#for i in range(0, len(t.columns)):
#  c = t.cell(0, i)
#  print(c.text)
#  for cha in c.text:
#    print(cha)
#    print(ord(cha))
# %%
