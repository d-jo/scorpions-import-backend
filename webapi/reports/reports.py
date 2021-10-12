from flask import Blueprint, current_app
import os, glob
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

reports_bp = Blueprint("reports_bp", __name__)

@reports_bp.route('/trigger_process', methods=['GET'])
def trigger_process_files():
  for f in glob.glob(os.path.join(current_app.config['UPLOAD_FOLDER'], '*.txt')):
    with open(f, 'r') as file:
      # TODO change this to use the document parsing funciton
      # python is sometimes hard to work with multiple files unless the project
      # is set up a current way so we will deal with that later
      print("=====")
      print(file.read())
      print("=====")
  return { "message":"success" }
