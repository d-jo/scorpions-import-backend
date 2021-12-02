/* 
  === GRAD+UNDERGRAD 2019 REGULAR/NONACCREDITED ===
  TODO need information between tables
  DOCUMENT
    College
    Department
    Program
    Degree Level
    Academic Year
    Date range
    Author
    Additional information

  UNALLOCATED:
    2019:
      B. SLOs reflect profession standards...
    C (B 2018). Stakeholders involvement/communication

  SLO
    Description
    Bloom
    Graduate only:
      "Common graduate program slos"
    
  MEASURE
    Associated SLO
    1. Title
    2. Description of how measure aligns to slo
    3. Domain
    4. Type
    5. Point in Program
    6. Population Measured
    7. Frequency of collection
    8. Proffciency Threshold 
    9. Proffciency Target

  DATA COLLECTION AND ANALYSIS
    SLO
    Data collection date range
    Number of students assessed
    Percentage who met/exceeded
      

  DECISIONS + ACTIONS
    SLO
    Raw text or split each section (process, makers, timelines etc)
  

  === ACCREDITED ===

  DOCUMENT
    College
    Department
    Program
    Degree Level
    Academic Year
    Author
    Accredidation Body
    Last Accreditation review (next as well?)
    ADDITIONAL information
  
  SLO
    Description
    Bloom
    Graduate only:
      "Common graduate program slos"
  
  METHODS
    SLO
    Measure
    Domain
    Data collection

  ANALYSIS
    SLO
    Status (met, partially met, not met, unknown)
  
  DECISIONS/ACTIONS
    SLO
    Content?

*/

CREATE TABLE Report (
  id SERIAL NOT NULL,
  valid BOOLEAN NOT NULL,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  created INT NOT NULL,
  has_been_reviewed BOOLEAN NOT NULL,
  college TEXT NOT NULL,
  department TEXT NOT NULL,
  program TEXT NOT NULL,
  date_range TEXT NOT NULL,
  degree_level TEXT NOT NULL,
  academic_year TEXT NOT NULL,
  accreditation_body TEXT,
  last_accreditation_review TEXT,
  slos_meet_standards TEXT,
  stakeholder_involvement TEXT,
  additional_information TEXT,
  creator_id TEXT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE SLO (
  id SERIAL NOT NULL,
  report_id INT NOT NULL,
  description TEXT NOT NULL,
  bloom TEXT NOT NULL,
  common_graduate_program_slo TEXT,
  PRIMARY KEY (id),
  FOREIGN KEY (report_id) REFERENCES Report(id) ON DELETE CASCADE
);

CREATE TABLE Measure (
  id SERIAL NOT NULL,
  slo_id INT NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  domain TEXT NOT NULL,
  type TEXT NOT NULL,
  point_in_program TEXT NOT NULL,
  population_measured TEXT NOT NULL,
  frequency_of_collection TEXT NOT NULL,
  proficiency_threshold TEXT NOT NULL,
  proficiency_target TEXT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (slo_id) REFERENCES SLO(id) ON DELETE CASCADE
);

CREATE TABLE DecisionsActions (
  id SERIAL NOT NULL,
  slo_id INT NOT NULL,
  content TEXT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (slo_id) REFERENCES SLO(id) ON DELETE CASCADE
);

CREATE TABLE CollectionAnalysis (
  id SERIAL NOT NULL,
  slo_id INT NOT NULL,
  data_collection_date_range TEXT NOT NULL,
  number_of_students_assessed TEXT NOT NULL,
  percentage_who_met_or_exceeded TEXT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (slo_id) REFERENCES SLO(id) ON DELETE CASCADE
);

CREATE TABLE Methods (
  id SERIAL NOT NULL,
  slo_id INT NOT NULL,
  measure TEXT NOT NULL,
  domain TEXT NOT NULL,
  data_collection TEXT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (slo_id) REFERENCES SLO(id) ON DELETE CASCADE
);

CREATE TABLE AccreditedDataAnalysis (
  id SERIAL NOT NULL,
  slo_id INT NOT NULL,
  status TEXT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (slo_id) REFERENCES SLO(id) ON DELETE CASCADE
);

CREATE TABLE AuditLog (
  audit_id SERIAL NOT NULL,
  report_id INT NOT NULL,
  editor_name TEXT NOT NULL,
  timestamp BIGINT NOT NULL,
  action TEXT NOT NULL,
  PRIMARY KEY (audit_id),
  FOREIGN KEY (report_id) REFERENCES Report(id) ON DELETE CASCADE
);