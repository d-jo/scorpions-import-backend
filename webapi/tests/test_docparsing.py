import xml.etree.ElementTree as ET
import sys
sys.path.append('scorpions-import-backend/weapi/files')
from files.document_processing import get_report_info

def test_parse_xml():
  tree = ET.parse('./data/document.xml')
  results=get_report_info(tree.getroot())
  hasCheck=False
  for a in results:
    if "checkbox" in a:
     hasCheck=True
     break
  assert hasCheck
    
    