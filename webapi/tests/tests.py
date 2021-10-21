import xml.etree.ElementTree as ET
import sys
sys.path.append('/scorpions-import-backend/webapi/files')
from files.document_processing import rec_traverse

# %%
def test_parse_xml():
  tree=ET.parse('./data/document.xml')
  results = rec_traverse(tree.getroot())
  hasCheck = False
  for a in results:
    if "checkbox" in a:
      hasCheck = True
      break
  assert hasCheck
# %%
