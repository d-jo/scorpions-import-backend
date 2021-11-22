from docx.api import Document
from flask import Blueprint, current_app
import os, glob
from typing import Callable, AnyStr, List, Dict
from flask import Flask, flash, request, redirect, url_for, _request_ctx_stack,jsonify
from werkzeug.utils import secure_filename
import files.document_processing as processor
from models.model import *
from auth.auth import requires_auth
from database.driver import db_init
from auth.auth import requires_auth, get_token_auth_header

# from webapi.files import document_processing

reports_bp = Blueprint("reports_bp", __name__)

@reports_bp.route('/extract_data', methods=['POST'])
@requires_auth
def extract_data():
  #print("here")
  # for getting current user details
  # sub is current user id
  #print(_request_ctx_stack.top.current_user)

  cu = _request_ctx_stack.top.current_user
  editor_id = cu['sub']
  user_full_name = current_app.config['auth0_web_api'].get_user_name(editor_id)

  results = []
  for filename in request.json:
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER']) + "/" +filename
    rep_slo = processor.process_report(filepath)
    buf = rep_slo[0]
    buf.creator_id = editor_id
    rep_slo[0] = buf
    file_id = send_to_db(rep_slo, "acc" if 'accredited' in filename else "non")
    # audit log entry creation
    audit_entry = AuditLog(file_id, user_full_name, "extract")
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

@reports_bp.route('/<string:id>', methods=['GET', 'POST', 'DELETE'])
@requires_auth
def handle_report(id):
  
  editor_id = _request_ctx_stack.top.current_user['sub']

  is_aac = current_app.config['auth0_web_api'].user_has_role(editor_id, "aac", "impossible_role_id")

  if not is_aac:
    if not current_app.config['report_repo'].has_access_to_report(id, editor_id):
      # no access
      return {"status": "error", "message": "You do not have access to this report"}

  report = current_app.config['report_repo'].select_by_id(id)
  # GET a specific report by id
  if request.method == 'GET':
    response = report.to_dict()
    response['slos'] = []
    all_slos = current_app.config['slo_repo'].select_by_report_id(id)
    for s in all_slos:
      slo_obj = s.to_dict()
      # get measures
      measures = current_app.config['measure_repo'].select_by_slo_id(s.id)
      slo_obj['measures'] = [x.to_dict() for x in measures]
      # get decisionactions
      da = current_app.config['decisions_actions_repo'].select_by_slo_id(s.id)
      slo_obj['decision_actions'] = [x.to_dict() for x in da]
      # get collectionanalysis
      ca = current_app.config['collection_analysis_repo'].select_by_slo_id(s.id)
      slo_obj['collection_analyses'] = [x.to_dict() for x in ca]
      # get methods
      methods = current_app.config['methods_repo'].select_by_slo_id(s.id)
      slo_obj['methods'] = [x.to_dict() for x in methods]
      # get accrediteddataanalysis
      ada = current_app.config['accredited_data_analysis_repo'].select_by_slo_id(s.id)
      slo_obj['accredited_data_analyses'] = [x.to_dict() for x in ada]

      response['slos'].append(slo_obj)

    return response
  elif request.method == 'POST':
    # UPDATE a data by id
    data = request.json

    # report
    new_rep = Report()
    new_rep.init_from_dict(data)

    for s in data['slos']:
      # slo
      new_slo = SLO()
      new_slo.init_from_dict(s)
      current_app.config['slo_repo'].update(new_slo)

      # measures
      for m in s['measures']:
        new_measure = Measure()
        new_measure.init_from_dict(m)
        current_app.config['measure_repo'].update(new_measure)
      
      for da in s['decision_actions']:
        new_da = DecisionsAction()
        new_da.init_from_dict(da)
        current_app.config['decisions_actions_repo'].update(new_da)
      
      for ca in s['collection_analyses']:
        new_ca = CollectionAnalysis()
        new_ca.init_from_dict(ca)
        current_app.config['collection_analysis_repo'].update(new_ca)

      for m in s['methods']:
        new_method = Methods()
        new_method.init_from_dict(m)
        current_app.config['methods_repo'].update(new_method)
      
      for ada in s['accredited_data_analyses']:
        new_ada = AccreditedDataAnalysis()
        new_ada.init_from_dict(ada)
        current_app.config['accredited_data_analysis_repo'].update(new_ada)
      
    current_app.config['report_repo'].update(new_rep)

    # add entry in audit log
    cu = _request_ctx_stack.top.current_user

    # audit log entry creation
    editor_id = cu['sub']
    user_full_name = current_app.config['auth0_web_api'].get_user_name(editor_id)
    audit_entry = AuditLog(id, user_full_name, "update")
    current_app.config['audit_log_repo'].insert(audit_entry)
    # audit log complete 
    return {"status": "success", "message": "report updated"}
  elif request.method == 'DELETE':
    # DELETE a data    
    current_app.config['report_repo'].remove_report(id)
    # add entry in audit log
    cu = _request_ctx_stack.top.current_user

    # audit log entry creation
    editor_id = cu['sub']
    user_full_name = current_app.config['auth0_web_api'].get_user_name(editor_id)
    audit_entry = AuditLog(id, user_full_name, "delete")
    current_app.config['audit_log_repo'].insert(audit_entry)
    # audit log complete 
    return { "status": "success", "message": "deleted"}