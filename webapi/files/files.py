from flask import Blueprint, current_app
import os, glob
from flask import Flask, flash, request, redirect, url_for, _request_ctx_stack
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from auth.auth import requires_auth

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
  print('Recieved request: ' + request.method)
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
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
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
  file_list = os.listdir(current_app.config['UPLOAD_FOLDER'])

  cu = _request_ctx_stack.top.current_user
  asker = cu['sub']

  is_aac = current_app.config['auth0_web_api'].user_has_role(asker, "aac", "impossible_role_id")

  to_be_reviewed = None
  complete = None

  if is_aac:
    with current_app.config['db'] as (conn, cur):
      cur.execute("SELECT program, academic_year FROM report WHERE has_been_reviewed=FALSE AND valid=TRUE")
      conn.commit()
      to_be_reviewed = cur.fetchall()
      cur.execute("SELECT program, academic_year FROM report WHERE has_been_reviewed=TRUE AND valid=TRUE")
      conn.commit()
      complete = cur.fetchall()
  else:
    with current_app.config['db'] as (conn, cur):
      cur.execute("SELECT program, academic_year FROM report WHERE has_been_reviewed=FALSE AND creator_id=%(creator_id)s AND valid=TRUE", {"creator_id": asker})
      conn.commit()
      to_be_reviewed = cur.fetchall()
      cur.execute("SELECT program, academic_year FROM report WHERE has_been_reviewed=TRUE AND creator_id=%(creator_id)s AND valid=TRUE", {"creator_id": asker})
      conn.commit()
      complete = cur.fetchall()

  return {
            "uploaded":file_list,
            "review": to_be_reviewed,
            "done": complete,
        }



@views_bp.route('/<file_id>', methods=['GET'])
@requires_auth
def view_file(file_id):
  return {
            "academic_year": "2018-19",
            "accreditation_body": "",
            "additional_information": "",
            "author": "Andrew W Swift",
            "college": "Arts & Sciences",
            "created": 1637015615,
            "date_range": "2016-2018",
            "degree_level": "Masters",
            "department": "Mathematics",
            "has_been_reviewed": False,
            "id": "",
            "last_accreditation_review": "",
            "program": "MS",
            "slos_meet_standards": "",
            "stakeholder_involvement": "",
            "title": "",
            "slos": [
                {
                    "bloom": ["Application"],
                    "common_graduate_program_slo": ["1"],
                    "description": "Mastery of discipline content",
                    "id": "",
                    "report_id": 1
                },
                {
                    "bloom": ["Evaluation"],
                    "common_graduate_program_slo": ["2"],
                    "description": "Proficiency in analyzing, evaluating, and synthesizing information",
                    "id": "",
                    "report_id": 1
                },
                {
                    "bloom": ["Evaluation"],
                    "common_graduate_program_slo": ["3"],
                    "description": "Effective oral and written communication",
                    "id": "",
                    "report_id": 1
                },
                {
                    "bloom": ["Knowledge"],
                    "common_graduate_program_slo": ["4"],
                    "description": "Demonstrate knowledge of discipline’s ethics and standards",
                    "id": "",
                    "report_id": 1
                }
            ]
        }

  