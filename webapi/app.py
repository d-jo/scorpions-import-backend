import os, glob
import errno
from flask import Flask, flash, request, jsonify,redirect, url_for
from werkzeug.utils import secure_filename
from files.files import files_bp, views_bp, dashboard_bp
from reports.reports import reports_bp
from database.driver import db_init
import json
from audits.audits import audit_bp
from statistics.statistics import statistic_bp
from users.users import users_bp
from flask_cors import CORS
from auth.auth import requires_auth, AuthError, requires_scope
TARGET_FOLDER = './data'

app = Flask(__name__)


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
 
# ====== LOAD CONFIG ====== 
with open('config.json') as config_file:
    config = json.load(config_file)
    for key in config:
        app.config[key] = config[key]

with open('creds.json') as creds_file:
    creds = json.load(creds_file)
    app.secret_key = creds['secret_key']
    app.config['creds'] = creds


## create the database helper and add it to the config
with app.app_context():
    db_init()

    # Create upload folder if it doesn't exist
if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'])):
    try:
        os.mkdir(app.config['UPLOAD_FOLDER'])
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, Access-Control-Allow-Origin')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response


app.register_blueprint(files_bp, url_prefix="/files")
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
app.register_blueprint(views_bp, url_prefix="/view")
app.register_blueprint(reports_bp, url_prefix="/reports")
app.register_blueprint(audit_bp, url_prefix="/audit")
app.register_blueprint(statistic_bp, url_prefix="/statistics")
app.register_blueprint(users_bp, url_prefix="/users")
