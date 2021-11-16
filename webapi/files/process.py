from . import document_processing
from models.model import *

files = ["./old/data/grad2018-regular.docx", "./old/data/undergrad2018-regular.docx", "./old/data/grad2019-regular.docx", "./old/data/undergrad2019-regular.docx"]
# files = ["./old/data/grad2019-regular.docx"]
# files = ["./old/data/undergrad2019-regular.docx"]

for filename in files:
    print("================ " + filename + " ================")
    data = document_processing.process_report(filename)
    report = data[0]
    slos = data[1]
    measures = data[2]
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
            print("SLO " + str(pos) + "ASSESSMENTS")
            for m in slom:
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
    else:
        print('report was none')
    print("================================================\n")