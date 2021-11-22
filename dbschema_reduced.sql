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
  title VARCHAR(255) NOT NULL,
  author VARCHAR(255) NOT NULL,
  created INT NOT NULL,
  has_been_reviewed BOOLEAN NOT NULL,
  college VARCHAR(255) NOT NULL,
  department VARCHAR(255) NOT NULL,
  program VARCHAR(255) NOT NULL,
  date_range VARCHAR(255) NOT NULL,
  degree_level VARCHAR(255) NOT NULL,
  academic_year VARCHAR(255) NOT NULL,
  accreditation_body VARCHAR(255),
  last_accreditation_review VARCHAR(255),
  slos_meet_standards VARCHAR(255),
  stakeholder_involvement TEXT,
  additional_information TEXT,
  PRIMARY KEY (id)
);

CREATE TABLE SLO (
  id SERIAL NOT NULL,
  report_id INT NOT NULL,
  description TEXT NOT NULL,
  bloom VARCHAR(255) NOT NULL,
  common_graduate_program_slo VARCHAR(255),
  PRIMARY KEY (id),
  FOREIGN KEY (report_id) REFERENCES Report(id) ON DELETE CASCADE
);

CREATE TABLE Measure (
  id SERIAL NOT NULL,
  slo_id INT NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  domain VARCHAR(255) NOT NULL,
  type VARCHAR(255) NOT NULL,
  point_in_program VARCHAR(255) NOT NULL,
  population_measured VARCHAR(255) NOT NULL,
  frequency_of_collection VARCHAR(255) NOT NULL,
  proficiency_threshold VARCHAR(255) NOT NULL,
  proficiency_target VARCHAR(255) NOT NULL,
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
  data_collection_date_range VARCHAR(255) NOT NULL,
  number_of_students_assessed INT NOT NULL,
  percentage_who_met_or_exceeded FLOAT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (slo_id) REFERENCES SLO(id) ON DELETE CASCADE
);

CREATE TABLE Methods (
  id SERIAL NOT NULL,
  slo_id INT NOT NULL,
  measure VARCHAR(255) NOT NULL,
  domain VARCHAR(255) NOT NULL,
  data_collection TEXT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (slo_id) REFERENCES SLO(id) ON DELETE CASCADE
);

CREATE TABLE AccreditedDataAnalysis (
  id SERIAL NOT NULL,
  slo_id INT NOT NULL,
  status VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (slo_id) REFERENCES SLO(id) ON DELETE CASCADE
);

CREATE TABLE AuditLog (
  audit_id SERIAL NOT NULL,
  report_id INT NOT NULL,
  editor_name VARCHAR(255) NOT NULL,
  timestamp BIGINT NOT NULL,
  action VARCHAR(255) NOT NULL,
  PRIMARY KEY (audit_id),
  FOREIGN KEY (report_id) REFERENCES Report(id) ON DELETE CASCADE
)