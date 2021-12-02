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

reports_bp = Blueprint("reports_bp", __name__)

@reports_bp.route('/extract_data', methods=['POST'])
@requires_auth
def extract_data():
  # for getting current user details
  # sub is current user id
  #print(_request_ctx_stack.top.current_user)

  cu = _request_ctx_stack.top.current_user
  editor_id = cu['sub']
  user_full_name = current_app.config['auth0_web_api'].get_user_name(editor_id)

  results = []
  for filename in request.json:
    # path to stub file in users dir
    asker_path = os.path.join(current_app.config['UPLOAD_FOLDER'], editor_id, filename)
    # path to full file in all
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], "all", filename)
    rep_slo = processor.process_report(filepath)
    buf = rep_slo[0]
    buf.creator_id = editor_id
    rep_slo[0] = buf
    file_id = send_to_db(rep_slo, "acc" if 'accredited' in filename else "non")
    # audit log entry creation
    audit_entry = AuditLog(file_id, user_full_name, "extract")
    current_app.config['audit_log_repo'].insert(audit_entry)
    # audit log complete 
    try:
      os.remove(filepath)
    except:
      pass
    
    try:
      os.remove(asker_path)
    except:
      pass

    results.append(rep_slo)

  docs = [] 
  slos = []
  measures = []
  analysis = []
  decisions = []
  for r in results:
    docs.append(retrieve_report_data(r))
    slos.append(retrieve_slo_data(r))
    measures.append(retrieve_measure_data(r))
    analysis.append(retrieve_analysis_data(r))
    decisions.append(retrieve_decisions_data(r))
  

  return { 
    "reports": docs, "slos": slos, 
    "measures": measures, "analysis": analysis, 
    "decisions": decisions 
  }

def send_to_db(obj: any, reportType: str) -> int:
  rep = obj[0]
  slo_list = obj[1]
  measures_list = obj[2]
  anaysis_list = obj[3]
  decisions_list = obj[4]
  slo_ids = []
  
  # insert report
  report_id = current_app.config['report_repo'].insert(rep, reportType)
  for slo in slo_list:
    slo.report_id = report_id
    slo_ids.append(current_app.config['slo_repo'].insert(slo))
      # which slo a measure/analysis/decision is tied to stored in the slo_id field until the slo is added, 
      # not all slos have a measure/analysis/decision and an slo may have more than one of each, 
      # so incrementally going up will not ork
  for measures in measures_list:
    for m in measures:
      m.slo_id = slo_ids[max(0, int(m.slo_id)-1)]
      current_app.config['measure_repo'].insert(m)
  for ac in anaysis_list:
    for a in ac:
      a.slo_id = slo_ids[max(0, int(a.slo_id)-1)]
      current_app.config['collection_analysis_repo'].insert(a) 
  for d in decisions_list:
    d.slo_id = slo_ids[max(0, int(d.slo_id)-1)]
    current_app.config['decisions_actions_repo'].insert(d)
  # TODO ?
  # current_app.config['methods_repo']
  return report_id

def retrieve_report_data(obj):
  data = []
  for item in obj:
    if isinstance(item, list):
      data.append(retrieve_report_data(item))
    if isinstance(item, Report):
      data.append(item.to_dict())
  return data

def retrieve_slo_data(obj):
  data = []
  for item in obj:
    if isinstance(item, list):
      data.append(retrieve_slo_data(item))
    if isinstance(item, SLO):
      data.append(item.to_dict())
  return data

def retrieve_measure_data(obj):
  data = []
  for item in obj:
    if isinstance(item, list):
      data.append(retrieve_slo_data(item))
    if isinstance(item, Measure):
      data.append(item.to_dict())
  return data

def retrieve_analysis_data(obj):
  data = []
  for item in obj:
    if isinstance(item, list):
      data.append(retrieve_slo_data(item))
    if isinstance(item, CollectionAnalysis):
      data.append(item.to_dict())
  return data
  
def retrieve_decisions_data(obj):
  data = []
  for item in obj:
    if isinstance(item, list):
      data.append(retrieve_slo_data(item))
    if isinstance(item, DecisionsAction):
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
    new_rep.has_been_reviewed = True

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


@reports_bp.route('/search', methods=['POST'])
@requires_auth
def search_reports():
  """
  Endpoint: /reports/search
  Method: POST
  Description: Searches select fields of reports. Returns
  three lists of results.

  Request format:
  { "search_key": "value" }

  Response format:
  {
    "done": [{report1...}, {report2...}, ...],
    "review": [{report1...}, {report2...}, ...],
    "uploaded": [{report1...}, {report2...}, ...]
  }
  """
  req_json = request.json

  if 'search_key' not in req_json:
    return {"status": "error", "message": "search_key not found in request"}
  
  search_key = req_json['search_key']

  cu = _request_ctx_stack.top.current_user
  editor_id = cu['sub']

  # get the request sender role and check if aac
  is_aac = current_app.config['auth0_web_api'].user_has_role(editor_id, "aac", "impossible_role_id")

  report_results = []

  if not is_aac:
    # do not return reports that the user does not have access to
    report_results = current_app.config['report_repo'].search_reports(search_key, editor_id)
  else:
    # editor is aac is admin
    # search all reports
    report_results = current_app.config['report_repo'].search_reports(search_key)
  
  to_be_reviewed = []
  done = []
  for r in report_results:
    if r.has_been_reviewed:
      done.append([r.id, r.program, r.academic_year])
    else:
      to_be_reviewed.append([r.id, r.program, r.academic_year])

  return {
            "uploaded": [],
            "review": to_be_reviewed,
            "done": done,
        }
  

