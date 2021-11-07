from flask import Blueprint
from flask import Flask, flash, request, redirect, url_for

audit_bp = Blueprint("audit_bp", __name__)


@audit_bp.route('/file/<file_id>', methods=['GET'])
def get_file_audit(file_id):
    return{
    "doc_id":file_id,
    "audit_trail":[
       {
          "doc_id":file_id,
          "status_text":"uploaded by",
          "username":"christian",
          "date_updated":"2021-10-18"
       },
       {
          "doc_id":file_id,
          "status_text":"processed by",
          "username":"declan",
          "date_updated":"2021-10-19"
       },
       {
          "doc_id":file_id,
          "status_text":"edited by",
          "username":"grant",
          "date_updated":"2021-10-20"
       },
       {
          "doc_id":file_id,
          "status_text":"approved by",
          "username":"vlad",
          "date_updated":"2021-10-21"
       }
    ]
 }

  