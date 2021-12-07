from flask import Blueprint, current_app
import os, glob
from typing import Callable, AnyStr, List, Dict
from flask import Flask, flash, request, redirect, url_for, _request_ctx_stack,jsonify
from werkzeug.utils import secure_filename
import files.document_processing as processor
from models.model import *
from auth.auth import requires_auth
from database.driver import db_init
import hashlib
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
  asker_hash = hashlib.md5(editor_id.encode('utf-8')).hexdigest()
  user_full_name = current_app.config['auth0_web_api'].get_user_name(editor_id)
  errors = []

  results = []
  print("files: ", request.json)
  for filename in request.json:
    try:
      # path to stub file in users dir
      asker_path = os.path.join(current_app.config['UPLOAD_FOLDER'], asker_hash, filename)
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

      results.append(rep_slo)

      try:
        os.remove(filepath)
      except:
        print("failed to remove filepath", filepath)
      
      try:
        os.remove(asker_path)
      except:
        print("failed to remove asker_path", asker_path)
    except Exception as e:
      print("!!!!!!!!!!!!!!!!!!! failed to process file:", filename, e)
      errors.append(str(e))
      #raise e
      continue

  docs = [] 
  slos = []
  measures = []
  analysis = []
  decisions = []
  methods = []
  adaList = []
  for r in results:
    docs.append(retrieve_data(r, Report))
    slos.append(retrieve_data(r, SLO))
    measures.append(retrieve_data(r, Measure))
    analysis.append(retrieve_data(r, CollectionAnalysis))
    decisions.append(retrieve_data(r, DecisionsAction))
    methods.append(retrieve_data(r, Methods))
    adaList.append(retrieve_data(r, AccreditedDataAnalysis))
  return { 
    "reports": docs, "slos": slos, 
    "measures": measures, "analysis": analysis, 
    "decisions": decisions, "methods" : methods, "ada" : adaList,
    "errors": errors
  }

def retrieve_data(obj, type):
  data = []
  for item in obj:
    if isinstance(item, list):
      data.append(retrieve_data(item, type))
    if isinstance(item, type):
      data.append(item.to_dict())
  return data

def send_to_db(obj: any, reportType: str) -> int:
  rep = obj[0]
  slo_list = obj[1]
  measures_list = obj[2]
  anaysis_list = obj[3]
  decisions_list = obj[4]
  methods_list = obj[5]
  ada_list = obj[6]
  slo_ids = []
  
  # insert report
  report_id = current_app.config['report_repo'].insert(rep, reportType)
  for slo in slo_list:
    slo.report_id = report_id
    slo.trim_fields()
    slo_ids.append(current_app.config['slo_repo'].insert(slo))
      # which slo a measure/analysis/decision is tied to stored in the slo_id field until the slo is added, 
      # not all slos have a measure/analysis/decision and an slo may have more than one of each, 
      # so incrementally going up will not ork
  for measures in measures_list:
    for m in measures:
      sloIdx = max(0, int(m.slo_id)-1)
      if(sloIdx < len(slo_ids)):
        m.slo_id = slo_ids[sloIdx]
        m.trim_fields()
        current_app.config['measure_repo'].insert(m)
  for ac in anaysis_list:
    for a in ac:
      sloIdx = max(0, int(a.slo_id)-1)
      if(sloIdx < len(slo_ids)):
        a.slo_id = slo_ids[sloIdx]
        a.trim_fields()
        current_app.config['collection_analysis_repo'].insert(a) 
  for d in decisions_list:
    sloIdx = max(0, int(d.slo_id)-1)
    if(sloIdx < len(slo_ids)):
      d.slo_id = slo_ids[sloIdx]
      d.trim_fields()
      current_app.config['decisions_actions_repo'].insert(d)
  for me in methods_list:
    sloIdx = max(0, int(me.slo_id)-1)
    if(sloIdx < len(slo_ids)):
      me.slo_id = slo_ids[sloIdx]
      me.trim_fields()
      current_app.config['methods_repo'].insert(me)
  for adaItem in ada_list:
    sloIdx = max(0, int(adaItem.slo_id)-1)
    if(sloIdx < len(slo_ids)):
      adaItem.slo_id = slo_ids[sloIdx]
      adaItem.trim_fields()
      current_app.config['accredited_data_analysis_repo'].insert(adaItem)
  return report_id

@reports_bp.route('/<string:id>', methods=['GET', 'POST', 'DELETE'])
@requires_auth
def handle_report(id):
  """
  Endpoint: /reports/<id>
  Method: GET, POST, DELETE

  GET Description: Given a report id, returns a report and all of its children
  as a dictionary.

  POST Description: Given a report id and a report in the same format as the GET endpoint,
  updates the report in the database. To add new non-slos, just make a dict
  with the desired attributes and send it as if it were being updated. MUST INCLUDE THE
  SLO ID IT SHOULD BE ASSOCIATED WITH. ALSO INCLUDE THE ATTRIBUTE "new": true TO TELL 
  THE DATABASE TO INSERT RATHER THAN UPDATE
  
  New SLOs can be created by adding SLOs to the report-level attribute
  'new_slos'. the new SLOs should have the same format as above and can also include new
  methods, decisions, measures, etc. The new SLOs will be added to the database and the
  children will also be added. 

  Example of adding new accredited_data_analysis:
  ```
    ...
      "slos": [
        {
          "id": 24,
            "accredited_data_analyses": [{
                "slo_id": 24,
                "status": "test12345",
                "new": true
            }],
          ...
  ```

  Example of adding new SLO:
  ```
  ...
  "id": 6,
  "new_slos": [
     {
            "accredited_data_analyses": [...],
            "bloom": "Analysis",
            "collection_analyses": [...],
            "common_graduate_program_slo": "",
            "decision_actions": [...],
            "description": "Demonstrates the ability to analyze and interpret texts in a senior paper or project",
            "id": 24,
            "measures": [...],
            "methods": [...],
            "report_id": 6
      }
    ]
    ...
  ```

  DELETE Description: Given a report id, sets the report as deleted in the database. This does not
  actually remove the report from the database for audit log reasons, so the report just has
  its 'valid' bit set to false and it is no longer returned in endpoints.

  """
  
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

    newSlos = None
    if 'new_slos' in data:
      newSlos = data['new_slos']

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
      if 'measures' in s:
        for m in s['measures']:
          new_measure = Measure()
          new_measure.init_from_dict(m)
          if 'new' in m and m['new']:
            # has slo_id, insert
            current_app.config['measure_repo'].insert(new_measure)
          else:
            current_app.config['measure_repo'].update(new_measure)
      
      if 'decision_actions' in s:
        for da in s['decision_actions']:
          new_da = DecisionsAction()
          new_da.init_from_dict(da)
          if 'new' in da and da['new']:
            # has slo_id, insert
            current_app.config['decisions_actions_repo'].insert(new_da)
          else:
            current_app.config['decisions_actions_repo'].update(new_da)
      
      if 'collection_analyses' in s:
        for ca in s['collection_analyses']:
          new_ca = CollectionAnalysis()
          new_ca.init_from_dict(ca)
          if 'new' in ca and ca['new']:
            # has slo_id, insert
            current_app.config['collection_analysis_repo'].insert(new_ca)
          else:
            current_app.config['collection_analysis_repo'].update(new_ca)

      if 'methods' in s:
        for m in s['methods']:
          new_method = Methods()
          new_method.init_from_dict(m)
          if 'new' in m and m['new']:
            # has slo_id, insert
            current_app.config['methods_repo'].insert(new_method)
          else:
            current_app.config['methods_repo'].update(new_method)
      
      if 'accredited_data_analyses' in s:
        for ada in s['accredited_data_analyses']:
          new_ada = AccreditedDataAnalysis()
          new_ada.init_from_dict(ada)
          if 'new' in ada and ada['new']:
            # has slo_id, insert
            current_app.config['accredited_data_analysis_repo'].insert(new_ada)
          else:
            current_app.config['accredited_data_analysis_repo'].update(new_ada)
      
    if newSlos is not None:
      for s in newSlos:
        # slo
        new_slo = SLO()
        new_slo.init_from_dict(s)  
        new_id = current_app.config['slo_repo'].insert(new_slo)

        # measures
        if 'measures' in s:
          for m in s['measures']:
            new_measure = Measure()
            new_measure.init_from_dict(m)
            new_measure.slo_id = new_id
            current_app.config['measure_repo'].insert(new_measure)
        
        if 'decision_actions' in s:
          for da in s['decision_actions']:
            new_da = DecisionsAction()
            new_da.init_from_dict(da)
            new_da.slo_id = new_id
            current_app.config['decisions_actions_repo'].insert(new_da)
        
        if 'collection_analyses' in s:
          for ca in s['collection_analyses']:
            new_ca = CollectionAnalysis()
            new_ca.init_from_dict(ca)
            new_ca.slo_id = new_id
            current_app.config['collection_analysis_repo'].insert(new_ca)

        if 'methods' in s:
          for m in s['methods']:
            new_method = Methods()
            new_method.init_from_dict(m)
            new_method.slo_id = new_id
            current_app.config['methods_repo'].insert(new_method)
        
        if 'accredited_data_analyses' in s:
          for ada in s['accredited_data_analyses']:
            new_ada = AccreditedDataAnalysis()
            new_ada.init_from_dict(ada)
            new_ada.slo_id = new_id
            current_app.config['accredited_data_analysis_repo'].insert(new_ada)
    
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
  

@reports_bp.route('/manage/<string:id>', methods=['POST'])
@requires_auth
def handle_manage(id):
  """
  Endpoint: /reports/manage/<id>
  Method: POST
  Description: Use this endpoint to remove SLOs or children of SLOs from a 
  report. Must either be the owner or an admin to successfuly remove something.

  Request format:
  {
    "remove_slos": [
      slo_id1, ...
    ],
    "remove_measure": [
      measure_id1, ...
    ],
    "remove_decision_action": [
      decision_action_id1, ...
    ],
    "remove_collection_analysis": [
      collection_analysis_id1, ...
    ],
    "remove_method": [
      method_id1, ...
    ],
    "remove_accredited_data_analysis": [
      accredited_data_analysis_id1, ...
    ]
  }

  Response format:
  {
    "status": "success",
    "message": "removed"
  }
  """
  data = request.json

  cu = _request_ctx_stack.top.current_user
  editor_id = cu['sub']

  # get the request sender role and check if aac
  is_aac = current_app.config['auth0_web_api'].user_has_role(editor_id, "aac", "impossible_role_id")

  is_report_owner = current_app.config['report_repo'].has_access_to_report(id, editor_id)

  if is_aac or is_report_owner:
    # editor is aac or report owner
    # remove slos
    if 'remove_slos' in data:
      for slo_id in data['remove_slos']:
        current_app.config['slo_repo'].delete(slo_id)
    
    # remove measures
    if 'remove_measure' in data:
      for measure_id in data['remove_measure']:
        current_app.config['measure_repo'].delete(measure_id)

    # remove decision actions
    if 'remove_decision_action' in data:
      for decision_action_id in data['remove_decision_action']:
        current_app.config['decisions_actions_repo'].delete(decision_action_id)

    # remove collection analyses
    if 'remove_collection_analysis' in data:
      for collection_analysis_id in data['remove_collection_analysis']:
        current_app.config['collection_analysis_repo'].delete(collection_analysis_id)

    # remove methods
    if 'remove_method' in data:
      for method_id in data['remove_method']:
        current_app.config['methods_repo'].delete(method_id)

    # remove accredited data analyses
    if 'remove_accredited_data_analysis' in data:
      for accredited_data_analysis_id in data['remove_accredited_data_analysis']:
        current_app.config['accredited_data_analysis_repo'].delete(accredited_data_analysis_id)

    # add entry in audit log
    cu = _request_ctx_stack.top.current_user

    # audit log entry creation
    editor_id = cu['sub']
    user_full_name = current_app.config['auth0_web_api'].get_user_name(editor_id)
    audit_entry = AuditLog(id, user_full_name, "remove_items")
    current_app.config['audit_log_repo'].insert(audit_entry)
    # audit log complete 
    return {"status": "success", "message": "removed"}
    
