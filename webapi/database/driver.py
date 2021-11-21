from flask import Blueprint, current_app
import psycopg2
import psycopg2.extras
import json


# https://www.psycopg.org/docs/extras.html

def _get_connection(username, password, host, database):
  """
  Gets a connection to the postgres database.
  """
  return psycopg2.connect(
    user = username,
    password = password,
    host = host,
    database = database
  )

def default_connection():
  return _get_connection( current_app.config['creds']['db_username'],
                          current_app.config['creds']['db_password'],
                          current_app.config['db_host'],
                          current_app.config['db_database'])
                
class AACDatabaseDriver():
  """
  AACDatabaseDriver is a helper class for getting a connection
  and cursor to the database. AACDatabaseDriver is a context manager
  and will close the cursor when it is done.

  usage:
  ```
  with AACDatabaseDriver() as (conn, cursor):
    cursor.execute(query)
    result = cursor.fetchall()
  ```
  """

  def __init__(self, connection, cursor_type=psycopg2.extras.DictCursor):
    """
    Initializes the AACDatabaseDriver using the given connection
    """
    self.conn = connection
    self.cursor_type=cursor_type
  
  def __enter__(self):
    """
    Sets up the context. Will return a tuple of the connection and cursor.

    Dont forget to call `conn.commit()` if you want your changes to be saved 
    to the DB. `conn.rollback()` will undo your changes.
    """
    # check to see if conn is none or closed
    # if so, create a new connection
    if self.conn is None or self.conn.closed:
      self.conn = default_connection()
    
    if self.cursor_type is None:
      # create a cursor
      self.current_cursor = self.conn.cursor()
    else:
      self.current_cursor = self.conn.cursor(cursor_factory=self.cursor_type)

    # return the connection and cursor
    return self.conn, self.current_cursor
  

  def __exit__(self, type, value, traceback):
    """
    Function for cleaning up the context. Will close the cursor.
    """
    #self.conn.commit()
    self.current_cursor.close()
  

  def __del__(self):
    """
    Will be run when the garbage collector runs. Need to close 
    the connection to the database.
    """
    if self.conn is not None and not self.conn.closed:
      self.conn.close()

from .repo import NewReportRepo, NewSLORepo, NewMeasureRepo, NewDecisionsActionsRepo, NewCollectionAnalysisRepo, NewMethodsRepo, NewAccreditedDataAnalysisRepo, NewAuditLogRepo, NewAuth0WebApi

def db_init():
  """
  Creates the database driver and adds it to the app context.
  """
  current_app.config['db'] = AACDatabaseDriver(default_connection())
  current_app.config['report_repo'] = NewReportRepo(current_app.config['db'])
  current_app.config['slo_repo'] = NewSLORepo(current_app.config['db'])
  current_app.config['measure_repo'] = NewMeasureRepo(current_app.config['db'])
  current_app.config['decisions_actions_repo'] = NewDecisionsActionsRepo(current_app.config['db'])
  current_app.config['collection_analysis_repo'] = NewCollectionAnalysisRepo(current_app.config['db'])
  current_app.config['methods_repo'] = NewMethodsRepo(current_app.config['db'])
  current_app.config['accredited_data_analysis_repo'] = NewAccreditedDataAnalysisRepo(current_app.config['db'])
  current_app.config['audit_log_repo'] = NewAuditLogRepo(current_app.config['db'])
  current_app.config['auth0_web_api'] = NewAuth0WebApi(current_app.config['creds']['AUTH0_MANAGEMENT_API_TOKEN'], current_app.config['creds']['AUTH0_MANAGEMENT_API_URL'])
  current_app.config['db_initialized'] = True

#db = _get_connection("aac_full", "aac_password", "localhost", "aac_db")
#aac = AACDatabaseDriver(db)
#
#with aac as (conn, cur):
#  cur.execute("SELECT * FROM users")


#c = db.cursor()
#c.execute("INSERT INTO slo(description, bloom) VALUES ('asdf', 'asdf')")
#db.commit()

# %%
