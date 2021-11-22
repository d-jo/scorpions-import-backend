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
    send_to_db(rep_slo, "acc" if 'accredited' in filename else "non")
    results.append(rep_slo)
  docs = [] 
  slos = []
  for r in results:
    docs.append(retrieve_report_data(r))
    slos.append(retrieve_slo_data(r))
  return { "reports": docs, "slos": slos }

def send_to_db(obj: any, reportType: str) -> None:
  rep = obj[0]
  slo_list = obj[1]
  # insert report
  report_id = current_app.config['report_repo'].insert(rep, reportType)
  for slo in slo_list:
    slo.report_id = report_id
    current_app.config['slo_repo'].insert(slo)
    
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

@reports_bp.route('/<string:id>', methods=['GET', 'POST', 'DELETE'])
#@requires_auth
def handle_report(id):
  report = current_app.config['report_repo'].select_by_id(id)
  # GET a specific report by id
  if request.method == 'GET':
    response = report.to_dict()
    response['slos'] = []
    all_slos = current_app.config['slo_repo'].select_by_report_id(id)
    for s in all_slos:
      slo_obj = s.to_dict()
      # TODO get other things
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
    # TODO
  elif request.method == 'DELETE':
    # DELETE a data    
    res = current_app.config['report_repo'].remove_report(id)
    print(res)
    return { "status": "success", "message": "deleted", "response": res}