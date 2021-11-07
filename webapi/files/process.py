import document_processing as processor

report = processor.process()
if report is not None:
    print("***** " + report.college + " *****\n")
    print("***** " + report.academicYear+ " *****\n")
    print("***** " + report.dateRange+ " *****\n")
    print("***** " + report.degreeLevel+ " *****\n")
    print("***** " + report.department+ " *****\n")
    print("***** " + report.personPreparing+ " *****\n")
    print("***** " + report.program+ " *****\n")
    print("***** " + " SLOS " + " *****")
    for slo in report.slos:
        print("***** "+ slo.title +" *****")
        print("***** "+ slo.bloomsTaxonomyLevel +" *****")
        print("***** "+ slo.commonGraduateSlos +" *****")
else:
    print('report was none')