from docx.api import Document
from flask import Blueprint, current_app
import os, glob
from typing import Callable, AnyStr, List, Dict
from flask import Flask, flash, request, redirect, url_for, _request_ctx_stack
from werkzeug.utils import secure_filename
import files.document_processing as processor
from models.model import *
from auth.auth import requires_auth

reports_bp = Blueprint("reports_bp", __name__)

@reports_bp.route('/trigger_process', methods=['GET'])
@requires_auth
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


@reports_bp.route('/<file_id>/edit', methods=['POST'])
@requires_auth
def edit_report(file_id):
  print(request.form)
  return { "message":"{} edited".format(file_id)  }

@reports_bp.route('/extract_data', methods=['POST'])
@requires_auth
def extract_data():
  # for getting current user details
  # sub is current user id
  results = []
  for filename in request.json:
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER']) + "/" +filename
    results.append(processor.process_report(filepath))
  docs = [] 
  slos = []
  for r in results:
    docs.append(retrieve_report_data(r))
    slos.append(retrieve_slo_data(r))
    send_to_db(r)
  return { "reports": docs, "slos": slos }

def send_to_db(obj: any) -> None:
  for item in obj:
    if isinstance(item, list):
      send_to_db(item)
    if isinstance(item, Report):
      print("calling report insert")
      current_app.config['report_repo'].insert(item, "non")
    if isinstance(item, SLO):
      print("calling insert")
      current_app.config['slo_repo'].insert(item)

def retrieve_report_data(obj):
  data = []
  for item in obj:
    if isinstance(item, list):
      data.append(retrieve_report_data(item))
    if isinstance(item, Report):
      print(item.department)
      data.append(item.to_dict())
  return data

def retrieve_slo_data(obj):
  data = []
  for item in obj:
    if isinstance(item, list):
      data.append(retrieve_slo_data(item))
    if isinstance(item, SLO):
      print(item.description)
      data.append(item.to_dict())
  return data
