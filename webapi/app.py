import os, glob
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from files.files import files_bp
from reports.reports import reports_bp
from database.driver import db_init
import json

TARGET_FOLDER = './data'

app = Flask(__name__)

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

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


app.register_blueprint(files_bp, url_prefix="/files")
app.register_blueprint(reports_bp, url_prefix="/reports")