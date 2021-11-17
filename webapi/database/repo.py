# %%
from models.model import BaseModel, SLO, Report, Measure, DecisionsAction, CollectionAnalysis, Methods, AccreditedDataAnalysis, AuditLog
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
  
def NewAccreditedDataAnalysisRepo(driver: AACDatabaseDriver) -> AccreditedDataAnalysisRepo:
  return AccreditedDataAnalysisRepo(driver)

class AuditLogRepo(Repository):

  def __init__(self, driver: AACDatabaseDriver):
    super().__init__(driver, "auditlog")
  
  def insert(self, audit_log: AuditLog) -> None:
    q = "INSERT INTO auditlog (report_id, editor_name, timestamp, action) VALUES (%(report_id)s, %(editor_name)s, %(timestamp)s, %(action)s)"
    self.named_exec(q, audit_log.to_dict())
  
def NewAuditLogRepo(driver: AACDatabaseDriver) -> AuditLogRepo:
  return AuditLogRepo(driver)


# %%

import requests

class Auth0WebApi():

  def __init__(self, token: str, base_url: str):
    self.base_url = base_url
    self.token = token

  def _make_request(self, url: str, request_type: str = "get", data: dict = None) -> dict:
    """
    Makes a request to the Auth0 API.
    """
    headers = {
      'Authorization': 'Bearer ' + self.token,
      'Content-Type': 'application/json'
    }
    if request_type == "get":
      r = requests.get(url, headers=headers)
    elif request_type == "post":
      r = requests.post(url, json=data, headers=headers)
    elif request_type == "put":
      r = requests.put(url, json=data, headers=headers)
    elif request_type == "delete":
      r = requests.delete(url, headers=headers, json=data)
    return r

  def get_user_info(self, uid: str) -> dict:
    """
    Returns a dictionary of the user's information.
    """
    #headers = {'Authorization': 'Bearer ' + self.token}
    #r = requests.get('{}/api/v2/users/{}'.format(self.base_url, uid), headers=headers)
    #return r.json()
    r = self._make_request('{}/api/v2/users/{}'.format(self.base_url, uid), "get")
    return r.json()
  
  def get_user_name(self, uid: str):
    """
    Returns the user's name.
    """
    uinfo = self.get_user_info(uid)
    return uinfo['given_name'] + " " + uinfo['family_name']
  
  def get_user_roles(self, uid: str):
    """
    Returns a list of the user's roles.
    """
    r = self._make_request('{}/api/v2/users/{}/roles'.format(self.base_url, uid), "get")
    return r
  
  def remove_user_role(self, uid: str, role: str):
    """
    Removes a role from the user with the provided uid
    """
    body = {
      "roles": [role]
    }
    r = self._make_request('{}/api/v2/users/{}/roles'.format(self.base_url, uid), "delete", body)
    return r.status_code
  
  def add_user_role(self, uid: str, role: str):
    """
    Adds a role to the user with the provided uid
    """
    body = {
      "roles": [role]
    }
    r = self._make_request('{}/api/v2/users/{}/roles'.format(self.base_url, uid), "post", body)
    return r.status_code

def NewAuth0WebApi(token: str, base_url: str) -> Auth0WebApi:
  return Auth0WebApi(token, base_url)

#token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFPZ3FZOUlCMkZuQ2d3NnVIMGNQbiJ9.eyJpc3MiOiJodHRwczovL2Rldi16LW5xYThzMC51cy5hdXRoMC5jb20vIiwic3ViIjoibUhsUW1UQ0FLWjdTTU8wZWhjUmo5bFdDNW1IaXpkSURAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vZGV2LXotbnFhOHMwLnVzLmF1dGgwLmNvbS9hcGkvdjIvIiwiaWF0IjoxNjM3MDk4OTIyLCJleHAiOjE2Mzc3MDM3MjIsImF6cCI6Im1IbFFtVENBS1o3U01PMGVoY1JqOWxXQzVtSGl6ZElEIiwic2NvcGUiOiJyZWFkOmNsaWVudF9ncmFudHMgY3JlYXRlOmNsaWVudF9ncmFudHMgZGVsZXRlOmNsaWVudF9ncmFudHMgdXBkYXRlOmNsaWVudF9ncmFudHMgcmVhZDp1c2VycyB1cGRhdGU6dXNlcnMgZGVsZXRlOnVzZXJzIGNyZWF0ZTp1c2VycyByZWFkOnVzZXJzX2FwcF9tZXRhZGF0YSB1cGRhdGU6dXNlcnNfYXBwX21ldGFkYXRhIGRlbGV0ZTp1c2Vyc19hcHBfbWV0YWRhdGEgY3JlYXRlOnVzZXJzX2FwcF9tZXRhZGF0YSByZWFkOnVzZXJfY3VzdG9tX2Jsb2NrcyBjcmVhdGU6dXNlcl9jdXN0b21fYmxvY2tzIGRlbGV0ZTp1c2VyX2N1c3RvbV9ibG9ja3MgY3JlYXRlOnVzZXJfdGlja2V0cyByZWFkOmNsaWVudHMgdXBkYXRlOmNsaWVudHMgZGVsZXRlOmNsaWVudHMgY3JlYXRlOmNsaWVudHMgcmVhZDpjbGllbnRfa2V5cyB1cGRhdGU6Y2xpZW50X2tleXMgZGVsZXRlOmNsaWVudF9rZXlzIGNyZWF0ZTpjbGllbnRfa2V5cyByZWFkOmNvbm5lY3Rpb25zIHVwZGF0ZTpjb25uZWN0aW9ucyBkZWxldGU6Y29ubmVjdGlvbnMgY3JlYXRlOmNvbm5lY3Rpb25zIHJlYWQ6cmVzb3VyY2Vfc2VydmVycyB1cGRhdGU6cmVzb3VyY2Vfc2VydmVycyBkZWxldGU6cmVzb3VyY2Vfc2VydmVycyBjcmVhdGU6cmVzb3VyY2Vfc2VydmVycyByZWFkOmRldmljZV9jcmVkZW50aWFscyB1cGRhdGU6ZGV2aWNlX2NyZWRlbnRpYWxzIGRlbGV0ZTpkZXZpY2VfY3JlZGVudGlhbHMgY3JlYXRlOmRldmljZV9jcmVkZW50aWFscyByZWFkOnJ1bGVzIHVwZGF0ZTpydWxlcyBkZWxldGU6cnVsZXMgY3JlYXRlOnJ1bGVzIHJlYWQ6cnVsZXNfY29uZmlncyB1cGRhdGU6cnVsZXNfY29uZmlncyBkZWxldGU6cnVsZXNfY29uZmlncyByZWFkOmhvb2tzIHVwZGF0ZTpob29rcyBkZWxldGU6aG9va3MgY3JlYXRlOmhvb2tzIHJlYWQ6YWN0aW9ucyB1cGRhdGU6YWN0aW9ucyBkZWxldGU6YWN0aW9ucyBjcmVhdGU6YWN0aW9ucyByZWFkOmVtYWlsX3Byb3ZpZGVyIHVwZGF0ZTplbWFpbF9wcm92aWRlciBkZWxldGU6ZW1haWxfcHJvdmlkZXIgY3JlYXRlOmVtYWlsX3Byb3ZpZGVyIGJsYWNrbGlzdDp0b2tlbnMgcmVhZDpzdGF0cyByZWFkOmluc2lnaHRzIHJlYWQ6dGVuYW50X3NldHRpbmdzIHVwZGF0ZTp0ZW5hbnRfc2V0dGluZ3MgcmVhZDpsb2dzIHJlYWQ6bG9nc191c2VycyByZWFkOnNoaWVsZHMgY3JlYXRlOnNoaWVsZHMgdXBkYXRlOnNoaWVsZHMgZGVsZXRlOnNoaWVsZHMgcmVhZDphbm9tYWx5X2Jsb2NrcyBkZWxldGU6YW5vbWFseV9ibG9ja3MgdXBkYXRlOnRyaWdnZXJzIHJlYWQ6dHJpZ2dlcnMgcmVhZDpncmFudHMgZGVsZXRlOmdyYW50cyByZWFkOmd1YXJkaWFuX2ZhY3RvcnMgdXBkYXRlOmd1YXJkaWFuX2ZhY3RvcnMgcmVhZDpndWFyZGlhbl9lbnJvbGxtZW50cyBkZWxldGU6Z3VhcmRpYW5fZW5yb2xsbWVudHMgY3JlYXRlOmd1YXJkaWFuX2Vucm9sbG1lbnRfdGlja2V0cyByZWFkOnVzZXJfaWRwX3Rva2VucyBjcmVhdGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiBkZWxldGU6cGFzc3dvcmRzX2NoZWNraW5nX2pvYiByZWFkOmN1c3RvbV9kb21haW5zIGRlbGV0ZTpjdXN0b21fZG9tYWlucyBjcmVhdGU6Y3VzdG9tX2RvbWFpbnMgdXBkYXRlOmN1c3RvbV9kb21haW5zIHJlYWQ6ZW1haWxfdGVtcGxhdGVzIGNyZWF0ZTplbWFpbF90ZW1wbGF0ZXMgdXBkYXRlOmVtYWlsX3RlbXBsYXRlcyByZWFkOm1mYV9wb2xpY2llcyB1cGRhdGU6bWZhX3BvbGljaWVzIHJlYWQ6cm9sZXMgY3JlYXRlOnJvbGVzIGRlbGV0ZTpyb2xlcyB1cGRhdGU6cm9sZXMgcmVhZDpwcm9tcHRzIHVwZGF0ZTpwcm9tcHRzIHJlYWQ6YnJhbmRpbmcgdXBkYXRlOmJyYW5kaW5nIGRlbGV0ZTpicmFuZGluZyByZWFkOmxvZ19zdHJlYW1zIGNyZWF0ZTpsb2dfc3RyZWFtcyBkZWxldGU6bG9nX3N0cmVhbXMgdXBkYXRlOmxvZ19zdHJlYW1zIGNyZWF0ZTpzaWduaW5nX2tleXMgcmVhZDpzaWduaW5nX2tleXMgdXBkYXRlOnNpZ25pbmdfa2V5cyByZWFkOmxpbWl0cyB1cGRhdGU6bGltaXRzIGNyZWF0ZTpyb2xlX21lbWJlcnMgcmVhZDpyb2xlX21lbWJlcnMgZGVsZXRlOnJvbGVfbWVtYmVycyByZWFkOmVudGl0bGVtZW50cyByZWFkOmF0dGFja19wcm90ZWN0aW9uIHVwZGF0ZTphdHRhY2tfcHJvdGVjdGlvbiByZWFkOm9yZ2FuaXphdGlvbnMgdXBkYXRlOm9yZ2FuaXphdGlvbnMgY3JlYXRlOm9yZ2FuaXphdGlvbnMgZGVsZXRlOm9yZ2FuaXphdGlvbnMgY3JlYXRlOm9yZ2FuaXphdGlvbl9tZW1iZXJzIHJlYWQ6b3JnYW5pemF0aW9uX21lbWJlcnMgZGVsZXRlOm9yZ2FuaXphdGlvbl9tZW1iZXJzIGNyZWF0ZTpvcmdhbml6YXRpb25fY29ubmVjdGlvbnMgcmVhZDpvcmdhbml6YXRpb25fY29ubmVjdGlvbnMgdXBkYXRlOm9yZ2FuaXphdGlvbl9jb25uZWN0aW9ucyBkZWxldGU6b3JnYW5pemF0aW9uX2Nvbm5lY3Rpb25zIGNyZWF0ZTpvcmdhbml6YXRpb25fbWVtYmVyX3JvbGVzIHJlYWQ6b3JnYW5pemF0aW9uX21lbWJlcl9yb2xlcyBkZWxldGU6b3JnYW5pemF0aW9uX21lbWJlcl9yb2xlcyBjcmVhdGU6b3JnYW5pemF0aW9uX2ludml0YXRpb25zIHJlYWQ6b3JnYW5pemF0aW9uX2ludml0YXRpb25zIGRlbGV0ZTpvcmdhbml6YXRpb25faW52aXRhdGlvbnMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.L-_TAhCUjJuSzamTubhseocdBpqIDb-s0s-wUUHKZM5Y3_1qica3OQfvc_Z0otCSRMryrV7bwc80vkqFKUnboIpMO07BZJ7n_4KTjy5lD798cMbFFv4e6nkhookGPTjkf_K6PCFvxWsdXebqRuEx7FiOEDRIpONlUSRfjwdgOyxv5voT0EznzC5IUZMazcTtCIvohZ9EFZWqNKtXl66RT3wDu_w5k8py5b3V7PZhUVQ1rfj5dRWOX0EfeWPpNuwaEKYkIPSTVbcMnec-9SafAXaegweA3Bqo5rmBzGWdRMCjAEgP5Sx0UBRfoyDWpfygPBi76hP7lcSb2pcwExOfmg"
#base_url = "https://dev-z-nqa8s0.us.auth0.com"
#aow = Auth0WebApi(token, base_url)
#
#test = aow.get_user_info("google-oauth2|106277625010963196502")
#print(test)

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

 



    
# %%
