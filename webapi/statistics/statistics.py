from flask import Blueprint
from flask import Flask, flash, request, redirect, url_for
from auth.auth import requires_auth

statistic_bp = Blueprint("statistic_bp", __name__)
  
@statistic_bp.route('/', methods=['GET'])
@requires_auth
def get_statistics():
    return "mock statistic return"
  