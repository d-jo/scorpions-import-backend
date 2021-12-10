import xml.etree.ElementTree as ET
import sys
sys.path.append('/scorpions-import-backend/webapi/files')
from files.document_processing import process_report

# %%

def test_file_process():
    data = process_report("./data/test_file_proc.docx")
    report = data[0]
    slos = data[1]
    measures = data[2]
    anaysisList = data[3]
    decisions = data[4]
    methods = data[5]
    adaList = data[6]
    
    assert report is not None
    assert isinstance(report.college, str)
    assert isinstance(report.academic_year, str)
    assert isinstance(report.date_range, str)
    assert isinstance(report.degree_level, str)
    assert isinstance(report.department, str)
    assert isinstance(report.author, str)
    assert isinstance(report.program, str)

    assert report.college == 'College of IS&T'
    assert report.academic_year == '2021-2022'
    assert report.date_range == 'Spring 2018-Fall 2019'
    assert report.degree_level == 'BS'
    assert report.department == 'Scorpions'
    assert report.author == 'Team Scorpions'
    assert report.program == 'AAC Import'

    counter = 0
    for slo in slos:
        assert isinstance(slo.description, str)
        assert isinstance(slo.bloom, str)
        assert isinstance(slo.common_graduate_program_slo, str)
        if counter == 0:
            assert slo.description == 'This application was developed by Declan Johnson'
            assert slo.bloom == 'Knowledge'
            assert slo.common_graduate_program_slo == '1'
        if counter == 1:
            assert slo.description == 'As well as Grant McCarty'
            assert slo.bloom == 'Analysis'
            assert slo.common_graduate_program_slo == '2'
        if counter == 2:
            assert slo.description == 'Also developed by Christian Reza'
            assert slo.bloom == 'Comprehension'
            assert slo.common_graduate_program_slo == '3, 2'
        if counter == 3:
            assert slo.description == 'Along with Uladzimir Lahvinovich'
            assert slo.bloom == 'Evaluation'
            assert slo.common_graduate_program_slo == '1, 2'
        counter += 1
        pos = 1
        for slom in measures:
            for m in slom:
                assert isinstance(m.slo_id, str)
                assert isinstance(m.title, str)
                assert isinstance(m.description, str)
                assert isinstance(m.domain, str)
                assert isinstance(m.type, str)
                assert isinstance(m.point_in_program, str)
                assert isinstance(m.population_measured, str)
                assert isinstance(m.frequency_of_collection, str)
                assert isinstance(m.proficiency_threshold, str)
                assert isinstance(m.proficiency_target, str)
                if pos == 1:
                    assert m.slo_id == '1'
                    assert m.title == 'test measure for SLO 1'
                    assert m.description == 'this is a desc'
                    assert m.domain.strip() == 'Examination'
                    assert m.type.strip() == 'Direct  Measure'
                    assert m.point_in_program.strip() == 'In final term of program'
                    assert m.population_measured.strip() == 'All students'
                    assert m.frequency_of_collection.strip() == 'Once/semester'
                    assert m.proficiency_threshold == 'Describe: test threshold'
                    assert m.proficiency_target == 'Describe: test target'
                if pos == 2:
                    assert m.slo_id == '2'
                    assert m.title == 'second measure'
                    assert m.description == 'second desc for a measure, this is a desc, none of these check boxes even work.'
                    assert m.domain.strip() == ''
                    assert m.type.strip() == ''
                    assert m.point_in_program.strip() == ''
                    assert m.population_measured.strip() == ''
                    assert m.frequency_of_collection.strip() == ''
                    assert m.proficiency_threshold == 'Describe: test threshold for the second SLO'
                    assert m.proficiency_target == 'Describe: test target for the second SLO'
                if pos == 3:
                    assert m.slo_id == '3'
                    assert m.title == 'third measure'
                    assert m.description == 'Tapirs eat 75 pounds of food per day!'
                    assert m.domain.strip() == ''
                    assert m.type.strip() == ''
                    assert m.point_in_program.strip() == ''
                    assert m.population_measured.strip() == ''
                    assert m.frequency_of_collection.strip() == ''
                    assert m.proficiency_threshold == 'Describe: Tapirs are the largest mammal in South America'
                    assert m.proficiency_target == 'Describe: There are four species of Tapir'
                if pos == 4:
                    assert m.slo_id == '4'
                    assert m.title == 'fourth measure'
                    assert m.description == 'Tapirs are often called Living Fossils'
                    assert m.domain.strip() == ''
                    assert m.type.strip() == ''
                    assert m.point_in_program.strip() == ''
                    assert m.population_measured.strip() == ''
                    assert m.frequency_of_collection.strip() == ''
                    assert m.proficiency_threshold == 'Describe: The Tapir\'s closest Relatives Are Rhinos and Horses'
                    assert m.proficiency_target == 'Describe: Tapirs have a Prehensile Nose'
            pos += 1
        idx = 1
        for analysis in anaysisList:
            for a in analysis:
                assert isinstance(a.slo_id, str)
                assert isinstance(a.data_collection_date_range, str)
                assert isinstance(a.number_of_students_assessed, str)
                assert isinstance(a.percentage_who_met_or_exceeded, str)
                if idx == 1:
                    assert a.slo_id == '1'
                    assert a.data_collection_date_range == '2010'
                    assert a.number_of_students_assessed == '1'
                    assert a.percentage_who_met_or_exceeded == '10%'
                if idx == 2:
                    assert a.slo_id == '2'
                    assert a.data_collection_date_range == '2012'
                    assert a.number_of_students_assessed == '2'
                    assert a.percentage_who_met_or_exceeded == '20%'
                if idx == 3:
                    assert a.slo_id == '3'
                    assert a.data_collection_date_range == '2013'
                    assert a.number_of_students_assessed == '3'
                    assert a.percentage_who_met_or_exceeded == '30%'
                if idx == 4:
                    assert a.slo_id == '4'
                    assert a.data_collection_date_range == '2014'
                    assert a.number_of_students_assessed == '4'
                    assert a.percentage_who_met_or_exceeded == '40%'
            idx += 1
        decision = 1
        for d in decisions:
            assert isinstance(d.slo_id, str)
            assert isinstance(d.content, str)
            if decision == 1:
                assert d.slo_id == '1'
                assert d.content == "That long snout isn't just for looks. It's actually prehensile, meaning it's made to wrap around and grab things. Tapirs use their noses to grab fruit, leaves, and other food. For food that may seem out of reach, the creature can stretch its nose way up, wrap around the morsel and pull it down to eat."
            if decision == 2:
                assert d.slo_id == '2'
                assert d.content == "Tapirs take to the water to find additional forage. They not only swim well; they can also walk underwater, moving at a good clip along a lake bottom if needed. When alarmed, a tapir can even hide underwater and use its snout like a snorkel."
            if decision == 3:
                assert d.slo_id == '3'
                assert d.content == "Often called the \"gardeners of the forest,\" tapirs play an important role in dispersing seeds. They require a large range for foraging, and when they eat fruits and berries in one area and travel to the next, they take those seeds with them in their digestive tract and disperse them as they defecate. This helps boost the genetic diversity of plants in the forest. And because tapirs are large animals — South America's largest land mammal — they move a lot of seeds."
            if decision == 4:
                assert d.slo_id == '4'
                assert d.content == "Tapirs are among the most primitive mammals on Earth, having changed very little over the past 20 million years or so. The first fossil evidence of tapirs dates back to the Early Oligocene Epoch."
            decision += 1
        mth = 1
        for method in methods:
            assert isinstance(method.slo_id, str)
            assert isinstance(method.measure, str)
            assert isinstance(method.domain, str)
            assert isinstance(method.data_collection, str)
            # This report has no methods.
            if mth == 1:
                assert method.slo_id == ''
                assert method.measure == ''
                assert method.domain == ''
                assert method.data_collection == ''
            if mth == 2:
                assert method.slo_id == ''
                assert method.measure == ''
                assert method.domain == ''
                assert method.data_collection == ''
            if mth == 3:
                assert method.slo_id == ''
                assert method.measure == ''
                assert method.domain == ''
                assert method.data_collection == ''
            if mth == 4:
                assert method.slo_id == ''
                assert method.measure == ''
                assert method.domain == ''
                assert method.data_collection == ''
            mth += 1
        status = 1
        for a in adaList:
            assert isinstance(a.slo_id, str)
            assert isinstance(a.status, str)
            if status == 1:
                assert a.slo_id == '1'
                assert a.status == 'Partially Met'
            if status == 2:
                assert a.slo_id == '2'
                assert a.status == 'Met'
            if status == 3:
                assert a.slo_id == '3'
                assert a.status == 'Met'
            if status == 4:
                assert a.slo_id == '4'
                assert a.status == 'Partially Met'
            status += 1
        
