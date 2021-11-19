from docx.api import Document
from flask import Blueprint, current_app
import os, glob
from typing import Callable, AnyStr, List, Dict
from flask import Flask, flash, request, redirect, url_for, _request_ctx_stack
from werkzeug.utils import secure_filename
import files.document_processing as processor
from models.model import *
from auth.auth import requires_auth, get_token_auth_header

# from webapi.files import document_processing

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
  # add entry in audit log
  cu = _request_ctx_stack.top.current_user

  # audit log entry creation
  editor_id = cu.sub
  user_full_name = current_app.config['auth0_web_api'].get_user_name(editor_id)
  audit_entry = AuditLog(file_id, user_full_name, "edit")
  current_app.config['audit_log_repo'].insert(audit_entry)
  # audit log complete 
  return { "message":"{} edited".format(file_id)  }

@reports_bp.route('/<file_id>/delete', methods=['DELETE'])
@requires_auth
def delete_report(file_id):
  print(request.form)
  # add entry in audit log
  cu = _request_ctx_stack.top.current_user

  # audit log entry creation
  editor_id = cu.sub
  user_full_name = current_app.config['auth0_web_api'].get_user_name(editor_id)
  audit_entry = AuditLog(file_id, user_full_name, "delete")
  current_app.config['audit_log_repo'].insert(audit_entry)
  # audit log complete 
  return { "message":"{} edited".format(file_id)  }

@reports_bp.route('/extract_data', methods=['POST'])
@requires_auth
def extract_data():
  #print("here")
  # for getting current user details
  # sub is current user id
  #print(_request_ctx_stack.top.current_user)
  results = []
  for filename in request.json:
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER']) + "/" +filename
    rep_slo = processor.process_report(filepath)
    file_id = send_to_db(rep_slo, "acc" if 'accredited' in filename else "non")
    # audit log entry creation
    cu = _request_ctx_stack.top.current_user
    editor_id = cu.sub
    user_full_name = current_app.config['auth0_web_api'].get_user_name(editor_id)
    audit_entry = AuditLog(file_id, user_full_name, "delete")
    current_app.config['audit_log_repo'].insert(audit_entry)
    # audit log complete 
    results.append(rep_slo)

  docs = [] 
  slos = []
  for r in results:
    docs.append(retrieve_report_data(r))
    slos.append(retrieve_slo_data(r))


  return { "reports": docs, "slos": slos }

def send_to_db(obj: any, reportType: str) -> int:
  rep = obj[0]
  slo_list = obj[1]
  # insert report
  report_id = current_app.config['report_repo'].insert(rep, reportType)
  for slo in slo_list:
    slo.report_id = report_id
    current_app.config['slo_repo'].insert(slo)
  return report_id
  #for item in obj:
  #  if isinstance(item, list):
  #    send_to_db(item)
  #  if isinstance(item, Report):
  #    print("calling report insert")
  #    current_app.config['report_repo'].insert(item, "non")
  #  if isinstance(item, SLO):
  #    print("calling insert")
  #    current_app.config['slo_repo'].insert(item)

def retrieve_report_data(obj):
  data = []
  for item in obj:
    if isinstance(item, list):
      data.append(retrieve_report_data(item))
    if isinstance(item, Report):
      #print(item.department)
      data.append(item.to_dict())
  return data

def retrieve_slo_data(obj):
  data = []
  for item in obj:
    if isinstance(item, list):
      data.append(retrieve_slo_data(item))
    if isinstance(item, SLO):
      #print(item.description)
      data.append(item.to_dict())
  return data
