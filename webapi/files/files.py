from flask import Blueprint, current_app
import os, glob
from flask import Flask, flash, request, redirect, url_for, _request_ctx_stack
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from auth.auth import requires_auth
import hashlib

files_bp = Blueprint("files_bp", __name__)
views_bp = Blueprint("views_bp", __name__)
dashboard_bp = Blueprint("dashboard_bp", __name__)


ALLOWED_EXT = {'docx', 'pdf', 'txt'}

def is_allowed_ext(filename):
  allowed = False 
  for e in ALLOWED_EXT:
    if filename.endswith(e):
      return True
  return allowed

@files_bp.route('/', methods=['GET', 'POST'])
#@cross_origin(headers=["Content-Type", "Authorization"])
#@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
@requires_auth
def upload_file():

  cu = _request_ctx_stack.top.current_user
  asker = cu['sub']
  asker_hash = hashlib.md5(asker.encode('utf-8')).hexdigest()

  all_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], "all")
  asker_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], asker_hash)

  if not os.path.exists(all_dir):
    os.mkdir(all_dir)

  if not os.path.exists(asker_dir):
    os.makedirs(asker_dir)

  #is_aac = current_app.config['auth0_web_api'].user_has_role(asker, "aac", "impossible_role_id")

  if request.method == 'POST':
    if 'file' not in request.files:
      flash('no file part')
      return redirect(request.url)

    uploadedFiles = request.files.getlist("file")
    for file in uploadedFiles:
      if file.filename == "":
        flash('no selected file')
      if file and is_allowed_ext(file.filename):
        filename = secure_filename(file.filename)
        # save the actual file with contents to all
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], "all", filename))
        # save a stub in the users folder to signify access
        with open(os.path.join(current_app.config['UPLOAD_FOLDER'], asker_hash, filename), 'w') as f:
          pass

    return redirect(request.url)

  return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
  """

  
@dashboard_bp.route('/', methods=['GET'])
@requires_auth
def get_files():


  cu = _request_ctx_stack.top.current_user
  asker = cu['sub']
  asker_hash = hashlib.md5(asker.encode('utf-8')).hexdigest()

  is_aac = current_app.config['auth0_web_api'].user_has_role(asker, "aac", "impossible_role_id")
  asker_path = os.path.join(current_app.config['UPLOAD_FOLDER'], asker_hash)
  all_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'all')

  if not os.path.exists(asker_path):
    os.makedirs(asker_path)
  
  if not os.path.exists(all_path):
    os.makedirs(all_path)

  file_list = os.listdir(asker_path)
  # if they are aac, recursive over all dirs in UPLOAD_FODLER
  if is_aac:
    file_list = os.listdir(all_path)


  to_be_reviewed = None
  complete = None

  if is_aac:
    with current_app.config['db'] as (conn, cur):
      cur.execute("SELECT id, program, academic_year FROM report WHERE has_been_reviewed=FALSE AND valid=TRUE")
      conn.commit()
      to_be_reviewed = cur.fetchall()
      cur.execute("SELECT id, program, academic_year FROM report WHERE has_been_reviewed=TRUE AND valid=TRUE")
      conn.commit()
      complete = cur.fetchall()
  else:
    with current_app.config['db'] as (conn, cur):
      cur.execute("SELECT id, program, academic_year FROM report WHERE has_been_reviewed=FALSE AND creator_id=%(creator_id)s AND valid=TRUE", {"creator_id": asker})
      conn.commit()
      to_be_reviewed = cur.fetchall()
      cur.execute("SELECT id, program, academic_year FROM report WHERE has_been_reviewed=TRUE AND creator_id=%(creator_id)s AND valid=TRUE", {"creator_id": asker})
      conn.commit()
      complete = cur.fetchall()

  return {
            "uploaded":file_list,
            "review": to_be_reviewed,
            "done": complete,
        }

