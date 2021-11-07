from flask import Blueprint, current_app
import os, glob
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

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
def get_files():
  file_list = os.listdir(current_app.config['UPLOAD_FOLDER'])
  return {
            "uploaded":file_list,
            "review": [ "mockReview.docx" ],  # TODO call database to get files in the future
            "done": [ "mockDone.docx" ]
        }



@views_bp.route('/<file_id>', methods=['GET'])
def view_file(file_id):
  return "view file for fileId {}" .format(file_id)
  