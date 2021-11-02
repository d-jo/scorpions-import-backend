import os, glob
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from files.files import files_bp, views_bp, dashboard_bp
from reports.reports import reports_bp
from audits.audits import audit_bp
from statistics.statistics import statistic_bp

TARGET_FOLDER = './data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = TARGET_FOLDER
app.secret_key = "secret key"

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


app.register_blueprint(files_bp, url_prefix="/files")
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
app.register_blueprint(views_bp, url_prefix="/view")
app.register_blueprint(reports_bp, url_prefix="/reports")
app.register_blueprint(audit_bp, url_prefix="/audit")
app.register_blueprint(statistic_bp, url_prefix="/statistics")
