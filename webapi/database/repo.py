# %%
from models.model import BaseModel, SLO, Report, Measure, DecisionsAction, CollectionAnalysis, Methods, AccreditedDataAnalysis
from .driver import AACDatabaseDriver 
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
  
  def named_exec(self, q: AnyStr, argdict: Dict) -> List:
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
      print("doing named exec with:")
      print(q)
      print(argdict)
      cur.execute(q, argdict)
      conn.commit()

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
  
  def insert(self, doc: Report, type: AnyStr) -> None:
    """
    Inserts a document into the database. The type of document is specified by
    the type argument and can either be accredited or non-accredited.

    doc is the document to be inserted.
    """
    q = "INSERT INTO report (title, author, created, college, department, program, degree_level, academic_year, date_range, accreditation_body, last_accreditation_review, additional_information) VALUES (%(title)s, %(author)s, 100, %(college)s, %(department)s, %(program)s, %(degree_level)s, %(academic_year)s, %(date_range)s, %(accreditation_body)s, %(last_accreditation_review)s, %(additional_information)s)"
    if type.startswith('non'):
      q = "INSERT INTO report (title, author, created, college, department, program, degree_level, academic_year, date_range, slos_meet_standards, stakeholder_involvement, additional_information) VALUES (%(title)s, %(author)s, 100, %(college)s, %(department)s, %(program)s, %(degree_level)s, %(academic_year)s, %(date_range)s, %(slos_meet_standards)s, %(stakeholder_involvement)s, %(additional_information)s)"
    
    self.named_exec(q, doc.to_dict())
  
def NewReportRepo(driver: AACDatabaseDriver) -> ReportRepo:
  return ReportRepo(driver)
  
class SLORepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver, "slo")

  def insert(self, slo: SLO) -> None:
    """
    Inserts a SLO into the database.
    """
    q = "INSERT INTO slo (description, bloom) VALUES (%(description)s, %(bloom)s)"
    self.named_exec(q, slo.to_dict())

def NewSLORepo(driver: AACDatabaseDriver) -> SLORepo:
  return SLORepo(driver)

class MeasureRepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver)
  
  def insert(self, measure: Measure) -> None:
    """
    Inserts a measure into the database.
    """
    q = "INSERT INTO measure (slo_id, title, description, domain, type, point_in_program, population_measured, frequency_of_collection, proficency_threshold, proficiency_target) VALUES (%(slo_id)s, %(title)s, %(description)s, %(domain)s, %(type)s, %(point_in_program)s, %(population_measured)s, %(frequency_of_collection)s, %(proficency_threshold)s, %(proficiency_target)s)"
    self.named_exec(q, measure.to_dict())

def NewMeasureRepo(driver: AACDatabaseDriver) -> MeasureRepo:
  return MeasureRepo(driver)

class DecisionsActionsRepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver)
  
  def insert(self, decisions_actions: DecisionsAction) -> None:
    """
    Inserts a DA into the database.
    """
    q = "INSERT INTO decisionsactions (slo_id, content) VALUES (%(slo_id)s, %(content)s)"
    self.named_exec(q, decisions_actions.to_dict())

def NewDecisionsActionsRepo(driver: AACDatabaseDriver) -> MeasureRepo:
  return DecisionsActionsRepo(driver)

class CollectionAnalysisRepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver)
  
  def insert(self, ca: CollectionAnalysis) -> None:
    """
    Inserts a CA into the database.
    """
    q = "INSERT INTO collectionanalysis (slo_id, data_collection_date_range, number_of_students_assessed, percentage_who_met_or_exceeded) VALUES (%(slo_id)s, %(data_collection_date_range)s, %(number_of_students_assessed)s, %(percentage_who_met_or_exceeded)s)"
    self.named_exec(q, ca.to_dict())

def NewCollectionAnalysisRepo(driver: AACDatabaseDriver) -> MeasureRepo:
  return CollectionAnalysisRepo(driver)

class MethodsRepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver)
  
  def insert(self, method: Methods) -> None:
    """
    Inserts a method into the database.
    """
    q = "INSERT INTO methods (slo_id, measure, domain, data_collection) VALUES (%(slo_id)s, %(measure)s, %(domain)s, %(data_collection)s)"
    self.named_exec(q, method.to_dict())

def NewMethodsRepo(driver: AACDatabaseDriver) -> MethodsRepo:
  return MethodsRepo(driver)

class AccreditedDataAnalysisRepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver)
  
  def insert(self, ada: AccreditedDataAnalysis) -> None:
    """
    Inserts a ADA into the database.
    """
    q = "INSERT INTO accrediteddataanalysis (slo_id, status) VALUES (%(slo_id)s, %(status)s)"
    self.named_exec(q, ada.to_dict())
  
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

 



    