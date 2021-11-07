class Report:
    college = ""
    department = ""
    program = ""
    degreeLevel = ""
    academicYear = ""
    dateRange = ""
    personPreparing = ""
    def __init__(self):
        self.slos = []

class SLO:
    BLOOMSTAX = ["Knowledge", "Analysis", "Comprehension","Synthesis","Application", "Evaluation"]
    COMMONGRAD = ["1", "2", "3", "4", "Not applicable for SLO"]
    def __init__(self):
        self.title = ""
        self.bloomsTaxonomyLevel = ""
        self.commonGraduateSlos = ""
        self.reflect = False
        self.assessments = []

class Assessment:
    def __init__(self):
        self.titleofMeasure = ""
        self.measureAligns = ""
        self.domain = ""
        self.measureType = ""
        self.assessmentPoint = ""
        self.population = ""
        self.frequency = ""
        self.proficiencyThreshold = ""
        self.proficiencyTarget = ""