from . import document_processing
from models.model import *

files = ["./old/data/grad2018-regular.docx", "./old/data/undergrad2018-regular.docx", "./old/data/grad2019-regular.docx", "./old/data/undergrad2019-regular.docx"]

for filename in files:
    print("================ " + filename + " ================")
    data = document_processing.process_report(filename)
    report = data[0]
    slos = data[1]
    measures = data[2]
    anaysisList = data[3]
    decisions = data[4]

    if report is not None:
        print("***** " + report.title + " *****\n")
        print("***** " + report.college + " *****\n")
        print("***** " + report.academic_year+ " *****\n")
        print("***** " + report.date_range+ " *****\n")
        print("***** " + report.degree_level+ " *****\n")
        print("***** " + report.department+ " *****\n")
        print("***** " + report.author+ " *****\n")
        print("***** " + report.program+ " *****\n")
        print("***** " + " SLOS " + " *****")
        for slo in slos:
            print("***** "+ slo.description +" *****")
            print("***** "+ slo.bloom +" *****")
            print("***** "+ slo.common_graduate_program_slo +" *****")
        pos = 1
        for slom in measures:
            print("SLO " + str(pos) + " ASSESSMENTS")
            for m in slom:
                print("SLO ID*****" + m['slo_id'] +"*****")
                print("TITLE *****"+ m["title"] + "*****")
                print("DESC *****"+ m["description"] + "*****")
                print("DOMAIN *****"+ m["domain"] + "*****")
                print("TYPE *****"+ m["type"] + "*****")
                print("POINT *****"+ m["point_in_program"] + "*****")
                print("POP MEASURED *****"+ m["population_measured"] + "*****")
                print("FREQUENCY *****"+ m["frequency_of_collection"] + "*****")
                print("PROF THRES *****"+ m["proficiency_threshold"] + "*****")
                print("PROF TARGET *****"+ m["proficiency_target"] + "*****")
            pos += 1
        idx = 1
        for analysis in anaysisList:
            print("SLO " + str(idx) + " ANALYSIS")
            for a in analysis:
                print("SLO ID*****" + a.slo_id + "*****")
                print("DATE RANGE *****" +a.data_collection_date_range + "*****")
                print("# OF STUDENTS ASSESSED *****"+a.number_of_students_assessed+" *****")
                print("% WHO MET OR EXCEEDED *****"+a.percentage_who_met_or_exceeded+" *****")
            idx += 1
        for d in decisions:
            print("SLO ID*****" +d.slo_id + "*****")
            print("DECISIONS/ACTIONS *****" + d.content +"*****")
    else:
        print('report was none')
    print("================================================\n")