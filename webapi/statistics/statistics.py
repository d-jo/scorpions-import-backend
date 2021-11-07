from flask import Blueprint
from flask import Flask, flash, request, redirect, url_for

statistic_bp = Blueprint("statistic_bp", __name__)
  
@statistic_bp.route('/', methods=['GET'])
def get_statistics():
    return "mock statistic return"
  