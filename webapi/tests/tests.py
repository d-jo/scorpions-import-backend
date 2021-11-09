import xml.etree.ElementTree as ET
import sys
sys.path.append('/scorpions-import-backend/webapi/files')
from files.document_processing import rec_traverse, process_report

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

def test_file_process():
    data = process_report("./data/endpoint_word_doc.docx")
    report = data[0]
    slos = data[1]
    assert report is not None
    assert isinstance(report.college, str)
    assert isinstance(report.academic_year, str)
    assert isinstance(report.date_range, str)
    assert isinstance(report.degree_level, str)
    assert isinstance(report.department, str)
    assert isinstance(report.author, str)
    assert isinstance(report.program, str)

    assert report.college == 'Arts & Sciences'
    assert report.academic_year == '2018-19'
    assert report.date_range == '2016-2018'
    assert report.degree_level == 'Masters'
    assert report.department == 'Mathematics'
    assert report.author == 'Team Scorpions'
    assert report.program == 'MS'

    counter = 0
    for slo in slos:
        assert isinstance(slo.description, str)
        assert isinstance(slo.bloom, str)
        assert isinstance(slo.common_graduate_program_slo, str)
        if counter == 0:
            assert slo.description == 'Mastery of discipline content'
            assert slo.bloom == 'Application'
            assert slo.common_graduate_program_slo == '1'
        if counter == 1:
            assert slo.description == 'Proficiency in analyzing, evaluating, and synthesizing information'
            assert slo.bloom == 'Evaluation'
            assert slo.common_graduate_program_slo == '2'
        if counter == 2:
            assert slo.description == 'Effective oral and written communication'
            assert slo.bloom == 'Evaluation'
            assert slo.common_graduate_program_slo == '3'
        if counter == 3:
            assert slo.description == 'Demonstrate knowledge of discipline’s ethics and standards'
            assert slo.bloom == 'Knowledge'
            assert slo.common_graduate_program_slo == '4'
        counter += 1
