# %%
from webapi.database.driver import AACDatabaseDriver, _get_connection
from webapi.models.model import BaseModel, SLO, Document, Measure, DecisionsAction, CollectionAnalysis, Methods, AccreditedDataAnalysis
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
      cur.execute(q, argdict)
      conn.commit()

  def select_by_id(self, id: int) -> Document:
    """
    Selects a single document from the database by its id.
    """
    q = "SELECT * FROM {} WHERE id = %(id)s".format(self.table)
    return self.named_query(q, {'id': id}, Document)[0]
  
  def search(self, field: AnyStr, value: AnyStr) -> List[Document]:
    """
    Searches the database for documents that match the specified field and value.
    """
    q = "SELECT * FROM {} WHERE %(field)s = %(value)s".format(self.table)
    return self.named_query(q, {'field': field, 'value': value}, Document)
  

class DocumentRepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver, "document")
  
  def insert(self, doc: Document, type: AnyStr) -> None:
    """
    Inserts a document into the database. The type of document is specified by
    the type argument and can either be accredited or non-accredited.

    doc is the document to be inserted.
    """
    q = "INSERT INTO document (title, author, created, college, department, program, degree_level, academic_year, accreditation_body, last_accreditation_review, additional_information) VALUES (%(title)s, %(author)s, %(created)s, %(college)s, %(department)s, %(program)s, %(degree_level)s, %(academic_year)s, %(accreditation_body)s, %(last_accreditation_review)s, %(additional_information)s)"
    if type.startswith('non'):
      q = "INSERT INTO document (title, author, created, college, department, program, degree_level, academic_year, slos_meet_standards, stakeholder_involvement, additional_information) VALUES (%(title)s, %(author)s, %(created)s, %(college)s, %(department)s, %(program)s, %(degree_level)s, %(academic_year)s, %(slos_meet_standards)s, %(stakeholder_involvement)s, %(additional_information)s)"
    
    self.named_exec(q, doc.to_dict())
  
  
class SLORepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver, "slo")

  def insert(self, slo: SLO) -> None:
    """
    Inserts a SLO into the database.
    """
    q = "INSERT INTO slo (description, bloom) VALUES (%(description)s, %(bloom)s)"
    self.named_exec(q, slo.to_dict())

class MeasureRepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver)

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

 



    