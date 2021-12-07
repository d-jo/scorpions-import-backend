import xml.etree.ElementTree as ET
import sys
sys.path.append('/scorpions-import-backend/webapi/files')
from files.document_processing import process_report

# %%

def test_file_process():
    data = process_report("./data/grad2019-non-accredited.docx")
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

    assert report.college == 'CPACS'
    assert report.academic_year == '2019-2020'
    assert report.date_range == 'Spring 2018-Fall 2019'
    assert report.degree_level == 'Masters'
    assert report.department == 'Gerontology'
    assert report.author == 'Julie Blaskewicz Boron'
    assert report.program == 'MA Gerontology'

    counter = 0
    for slo in slos:
        assert isinstance(slo.description, str)
        assert isinstance(slo.bloom, str)
        assert isinstance(slo.common_graduate_program_slo, str)
        if counter == 0:
            assert slo.description == 'Analyze fundamental interdisciplinary evidence-based knowledge and theories for competent gerontological practice.'
            assert slo.bloom == 'Analysis'
            assert slo.common_graduate_program_slo == '1, 3, 2, 4'
        if counter == 1:
            assert slo.description == 'Critique and analyze diverse and complex aging issues and outcomes from an interdisciplinary perspective.'
            assert slo.bloom == 'Synthesis'
            assert slo.common_graduate_program_slo == '1, 2'
        if counter == 2:
            assert slo.description == 'Exhibit abilities to effectively use basic communication (written, oral, interpersonal) skills and information technology.'
            assert slo.bloom == 'Application'
            assert slo.common_graduate_program_slo == '3'
        if counter == 3:
            assert slo.description == 'Evaluate and appraise ability of oneself and others to demonstrate social and cultural awareness, sensitivity, respect, and support of multiple perspectives, and exhibit personal and social responsibility, and ethical and professional behavior in all settings.'
            assert slo.bloom == 'Synthesis'
            assert slo.common_graduate_program_slo == '1, 2, 4'
        counter += 1
        
