# %%
from models.model import BaseModel, SLO, Report, Measure, DecisionsAction, CollectionAnalysis, Methods, AccreditedDataAnalysis
from .driver import AACDatabaseDriver 
import time
from typing import Callable, AnyStr, List, Dict

# https://www.psycopg.org/docs/usage.html

class Repository():
  def __init__(self, driver: AACDatabaseDriver, table: AnyStr):
    self.driver = driver
    self.table = table

  def named_query(self, q: AnyStr, argdict: Dict, model_factory: Callable[[], BaseModel]) -> List:
    """
    q: should be a named query in the form below.

    argdict: should be a dictionary of arguments to be passed to the query and 
    must include every named variable in the query.

    modelfactory: should be a function that returns a model that is a child
    of BaseModel.
    
    Example named query: `"SELECT * FROM document  WHERE id = %(id)s"`

    The id field is a placeholder.
    """

    # TODO: check for exceptions

    with self.driver as (conn, cur):
      cur.execute(q, argdict)
      rows = cur.fetchall()

    reslist = []
    for row in rows:
      res = model_factory()
      res.init_from_dict(row)
      reslist.append(res)

    return reslist
  
  def named_exec(self, q: AnyStr, argdict: Dict, return_result=False) -> List:
    """
    q: should be a named query in the form below.

    argdict: should be a dictionary of arguments to be passed to the query and 
    must include every named variable in the query.

    Example named query: `"INSERT INTO slo (description, bloom) VALUES (%(description)s, %(bloom)s)"`

    In this example, the dict should contain the following keys:
      description: the description of the SLO
      bloom: the bloom level of the SLO
    """

    with self.driver as (conn, cur):
      cur.execute(q, argdict)
      conn.commit()
      if return_result:
        return cur.fetchall()
      else:
        return None

  def select_by_id(self, id: int) -> Report:
    """
    Selects a single document from the database by its id.
    """
    q = "SELECT * FROM {} WHERE id = %(id)s".format(self.table)
    return self.named_query(q, {'id': id}, Report)[0]
  
  def search(self, field: AnyStr, value: AnyStr) -> List[Report]:
    """
    Searches the database for documents that match the specified field and value.
    """
    q = "SELECT * FROM {} WHERE %(field)s = %(value)s".format(self.table)
    return self.named_query(q, {'field': field, 'value': value}, Report)
  

class ReportRepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver, "report")
  
  def insert(self, doc: Report, type: AnyStr) -> int:
    """
    Inserts a document into the database. The type of document is specified by
    the type argument and can either be accredited or non-accredited.

    doc is the document to be inserted.
    """
    q = "INSERT INTO report (title, author, created, college, department, program, degree_level, academic_year, date_range, accreditation_body, last_accreditation_review, additional_information, has_been_reviewed) VALUES (%(title)s, %(author)s, %(created)s, %(college)s, %(department)s, %(program)s, %(degree_level)s, %(academic_year)s, %(date_range)s, %(accreditation_body)s, %(last_accreditation_review)s, %(additional_information)s, FALSE) RETURNING id"
    if type.startswith('non'):
      q = "INSERT INTO report (title, author, created, college, department, program, degree_level, academic_year, date_range, slos_meet_standards, stakeholder_involvement, additional_information, has_been_reviewed) VALUES (%(title)s, %(author)s, %(created)s, %(college)s, %(department)s, %(program)s, %(degree_level)s, %(academic_year)s, %(date_range)s, %(slos_meet_standards)s, %(stakeholder_involvement)s, %(additional_information)s, FALSE) RETURNING id"
    
    doc.created = int(time.time())
    #doc.has_been_reviewed = False

    res = self.named_exec(q, doc.to_dict(), return_result=True)
    return res[0][0]
  
  def get_report_by_id(self, id: int) ->Report:
    """
    Selects a report from the database by id.
    """
    q = "SELECT title, author, created, college, department, program, degree_level, academic_year, date_range, accreditation_body, last_accreditation_review, additional_information, has_been_reviewed FROM report WHERE id = %(id)s"
    if type.startswith('non'):
     q = "SELECT title, author, created, college, department, program, degree_level, academic_year, date_range, slos_meet_standards, stakeholder_involvement, additional_information, has_been_reviewed FROM report WHERE id = %(id)s"     
    return self.named_query(q, {'id': id}, Report)[0]
  
  def update_report(self, id: int) ->Report:
      q="UPDATE report SET title = %(title)s, author=%(author)s, created = %(created)s, college=%(college)s, department= %(department)s, program =%(program)s, degree_level= %(degree_level)s, academic_year = %(academic_year)s, date_range=%(date_range)s, accreditation_body= %(accreditation_body)s, last_accreditation_review= %(last_accreditation_review)s, additional_information=%(additional_information)s, has_been_reviewed=%(has_been_reviewed)s WHERE id = %(id)s"  
    if type.startswith('non'):
      q="UPDATE report SET title = %(title)s, author=%(author)s, created = %(created)s, college=%(college)s, department= %(department)s, program =%(program)s, degree_level= %(degree_level)s, academic_year = %(academic_year)s, date_range=%(date_range)s, accreditation_body= %(accreditation_body)s, slos_meet_standards= %(slos_meet_standards)s, stakeholder_involvement=%(stakeholder_involvement)s, additional_information=%(additional_information)s WHERE id = %(id)s" 
    return self.named_query(q, {'id': id}, Report)[0]
  
  def remove_report(self, id: int) ->Report:      
   q="DELETE FROM report WHERE id = %(id)s"
     return self.named_query(q, {'id': id}, Report)[0]
 
def NewReportRepo(driver: AACDatabaseDriver) -> ReportRepo:
  return ReportRepo(driver)
  
class SLORepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver, "slo")

  def insert(self, slo: SLO) -> None:
    """
    Inserts a SLO into the database.
    """
    q = "INSERT INTO slo (report_id, description, bloom) VALUES (%(report_id)s, %(description)s, %(bloom)s)"
    self.named_exec(q, slo.to_dict(), return_result=False)
  
  def get_slo_by_report_id(self, id: int) ->SLO:
    """
    Selects a slo from the database by its id.
    """
    q = "SELECT description, bloom, common_graduate_program_slo FROM slo WHERE report_id = %(id)s"
    return self.named_query(q, {'id': id}, SLO)[0]
     
def NewSLORepo(driver: AACDatabaseDriver) -> SLORepo:
  return SLORepo(driver)

class MeasureRepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver, "measure")
  
  def insert(self, measure: Measure) -> None:
    """
    Inserts a measure into the database.
    """
    q = "INSERT INTO measure (slo_id, title, description, domain, type, point_in_program, population_measured, frequency_of_collection, proficency_threshold, proficiency_target) VALUES (%(slo_id)s, %(title)s, %(description)s, %(domain)s, %(type)s, %(point_in_program)s, %(population_measured)s, %(frequency_of_collection)s, %(proficency_threshold)s, %(proficiency_target)s)"
    self.named_exec(q, measure.to_dict())
    
  def get_measure_by_slo_id(self, id: int) -> Measure:
    """
    Selects a measure from the database by id.
    """
    q = "SELECT * FROM measure WHERE slo_id = %(id)s"
    return self.named_query(q, {'id': id}, Measure)[0]
  
def NewMeasureRepo(driver: AACDatabaseDriver) -> MeasureRepo:
  return MeasureRepo(driver)

class DecisionsActionsRepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver, "decisionsactions")
  
  def insert(self, decisions_actions: DecisionsAction) -> None:
    """
    Inserts a DA into the database.
    """
    q = "INSERT INTO decisionsactions (slo_id, content) VALUES (%(slo_id)s, %(content)s)"
    self.named_exec(q, decisions_actions.to_dict())
    
def get_decisionsactions_by_slo_id(self, id: int) ->DecisionsAction:
    """
    Selects a decisionsAction from the database by id.
    """
    q = "SELECT * FROM decisionsAction WHERE slo_id = %(id)s"
    return self.named_query(q, {'id': id}, DecisionsAction)[0]

def NewDecisionsActionsRepo(driver: AACDatabaseDriver) -> MeasureRepo:
  return DecisionsActionsRepo(driver)

class CollectionAnalysisRepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver, "collectionanalysis")
  
  def insert(self, ca: CollectionAnalysis) -> None:
    """
    Inserts a CA into the database.
    """
    q = "INSERT INTO collectionanalysis (slo_id, data_collection_date_range, number_of_students_assessed, percentage_who_met_or_exceeded) VALUES (%(slo_id)s, %(data_collection_date_range)s, %(number_of_students_assessed)s, %(percentage_who_met_or_exceeded)s)"
    self.named_exec(q, ca.to_dict())
    
def get_collectionAnalysis_by_slo_id(self, id: int) ->CollectionAnalysis:
    """
    Selects a CA from the database by id.
    """
    q = "SELECT * FROM collectionAnalysis WHERE slo_id = %(id)s"
    return self.named_query(q, {'id': id}, CollectionAnalysis)[0]
    
def NewCollectionAnalysisRepo(driver: AACDatabaseDriver) -> MeasureRepo:
  return CollectionAnalysisRepo(driver)

class MethodsRepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver, "methods")
  
  def insert(self, method: Methods) -> None:
    """
    Inserts a method into the database.
    """
    q = "INSERT INTO methods (slo_id, measure, domain, data_collection) VALUES (%(slo_id)s, %(measure)s, %(domain)s, %(data_collection)s)"
    self.named_exec(q, method.to_dict())
    
def get_methods_by_slo_id(self, id: int) ->Methods:
    """
    Selects a methods from the database by id.
    """
    q = "SELECT * FROM methods WHERE slo_id = %(id)s"
    return self.named_query(q, {'id': id}, Methods)[0]
  
def NewMethodsRepo(driver: AACDatabaseDriver) -> MethodsRepo:
  return MethodsRepo(driver)

class AccreditedDataAnalysisRepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver, "accrediteddataanalysis")
  
  def insert(self, ada: AccreditedDataAnalysis) -> None:
    """
    Inserts a ADA into the database.
    """
    q = "INSERT INTO accrediteddataanalysis (slo_id, status) VALUES (%(slo_id)s, %(status)s)"
    self.named_exec(q, ada.to_dict())
    
  def get_accreditedDataAnalysis_by_slo_id(self, id: int) ->AccreditedDataAnalysis:
    """
    Selects a accreditedDataAnalysis from the database by id.
    """
    q = "SELECT * FROM accreditedDataAnalysis WHERE slo_id = %(id)s"
    return self.named_query(q, {'id': id}, AccreditedDataAnalysis)[0]
  
def NewAccreditedDataAnalysisRepo(driver: AACDatabaseDriver) -> AccreditedDataAnalysisRepo:
  return AccreditedDataAnalysisRepo(driver)


#db = _get_connection("aac_full", "aac_password", "localhost", "aac_db")
#aac = AACDatabaseDriver(db)
#
#rep = Repository(aac)
#
#factory = lambda: SLO()
#q = "SELECT * FROM slo WHERE id = %(id)s"
#argdict = {'id': 5}
#
#resslo = rep.named_query(q, argdict, factory)
#
#print(resslo)
#print(resslo[0].id)
#print(resslo[0].description)
#print(resslo[0].bloom)


#class ReportRepo(Repository):
#
#  def __init__(self, driver: AACDatabaseDriver):
#    super().__init__(driver)

 



    