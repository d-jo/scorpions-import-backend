from . import document_processing
from webapi.models.model import *

for filename in ["./old/data/grad2018-regular.docx", "./old/data/undergrad2018-regular.docx", "./old/data/grad2019-regular.docx", "./old/data/undergrad2019-regular.docx"]:
    data = document_processing.process_report(filename)
    report = data[0]
    slos = data[1]
    if report is not None:
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
    else:
        print('report was none')