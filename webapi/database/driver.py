from flask import Blueprint, current_app
# %%
import psycopg2
import json

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

  def __init__(self, connection):
    """
    Initializes the AACDatabaseDriver using the given connection
    """
    self.conn = connection
  
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
    
    # create a cursor
    self.current_cursor = self.conn.cursor()

    # return the connection and cursor
    return self.conn, self.current_cursor
  

  def __exit__(self, type, value, traceback):
    """
    Function for cleaning up the context. Will close the cursor.
    """
    #self.conn.commit()
    self.current_cursor.close()
    return True
  

  def __del__(self):
    """
    Will be run when the garbage collector runs. Need to close 
    the connection to the database.
    """
    if self.conn is not None and not self.conn.closed:
      self.conn.close()

def db_init():
  """
  Creates the database driver and adds it to the app context.
  """
  current_app.config['db'] = AACDatabaseDriver(default_connection())

#db = _get_connection("aac_full", "aac_password", "localhost", "aac_db")
#aac = AACDatabaseDriver(db)
#
#with aac as (conn, cur):
#  cur.execute("SELECT * FROM users")


#c = db.cursor()
#c.execute("INSERT INTO slo(description, bloom) VALUES ('asdf', 'asdf')")
#db.commit()

# %%
