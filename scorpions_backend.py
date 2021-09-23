import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

TARGET_FOLDER = './data'
ALLOWED_EXT = {'docx', 'pdf', 'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = TARGET_FOLDER
app.secret_key = "secret key"

def is_allowed_ext(filename):
  allowed = False 
  for e in ALLOWED_EXT:
    if filename.endswith(e):
      return True
  return allowed

@app.route('/', methods=['POST'])
def upload_file():
  if 'file' not in request.files:
    flash('no file part')
    return redirect(request.url)
  
  file = request.files['file']

  if file.filename == "":
    flash('no selected file')
    return redirect(request.url)
  
  if file and is_allowed_ext(file.filename):
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('upload_file', name=filename))
  
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
