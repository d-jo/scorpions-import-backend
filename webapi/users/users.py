from flask import Blueprint
from flask import Flask, flash, request, redirect, url_for,  _request_ctx_stack, current_app
from auth.auth import requires_auth

users_bp = Blueprint("users_bp", __name__)
  
@users_bp.route('/all_users', methods=['GET'])
@requires_auth
def all_users():
  """
  Endpoint: /users/all_users
  Method: GET
  Description: Returns all users from the auth0 service.
  format:
  {
    "status": "success/error",
    "users": [{},{}...]
  }

  """
  cu = _request_ctx_stack.top.current_user
  editor_id = str(cu['sub'])

  # get the request sender role and check if aac
  is_aac = current_app.config['auth0_web_api'].user_has_role(editor_id, "aac", "impossible_role_id")

  if not is_aac:
    return {"status": "error", "message": "Only AACs can view list of users"}
  
  # get all users
  users = current_app.config['auth0_web_api'].get_users()

  return {"status": "success", "users": users}

@users_bp.route('/add_role', methods=['POST'])
@requires_auth
def add_role():
  """
  Endpoint: /users/add_role
  Method: POST
  Description: Adds a role to a user. Sender must be an AAC
  and the role id must exist (check config.json for roles 
  or check auth0 and get the role ID)

  Request format:
  {
    "uid": "target user_id",
    "desired_role_id": "role_id for their new role"
  }

  Response format:
  {
    "status": "success/error",
    "message": "message"
  }
  """
  req_json = request.json
  if "uid" not in req_json:
    return {"status": "error", "message": "uid not found in request"}
  
  if "desired_role_id" not in req_json:
    return {"status": "error", "message": "desired_role_id not found in request"}
  
  cu = _request_ctx_stack.top.current_user
  editor_id = cu['sub']

  # get the request sender role and check if aac
  is_aac = current_app.config['auth0_web_api'].user_has_role(editor_id, "aac", "impossible_role_id")

  if not is_aac:
    return {"status": "error", "message": "Only AACs can manage roles"}
  
  # add the users new role
  target_uid = req_json["uid"]
  target_role = req_json["desired_role_id"]

  result = current_app.config['auth0_web_api'].add_user_role(target_uid, target_role)

  if result == 204:
    return {"status": "success", "message": "role added"}
  else:
    return {"status": "error", "message": "role not added, status code: {}".format(result)}

  
  
@users_bp.route('/remove_role', methods=['POST'])
@requires_auth
def remove_role():
  """
  Endpoint: /users/remove_role
  Method: POST
  Description: Removes a role from a user. Sender must be an AAC
  and the role id must exist (check config.json for roles
  or check auth0 and get the role ID)

  Request format:
  {
    "uid": "target user_id",
    "desired_role_id": "role_id for the role to delete"
  }

  Response format:
  {
    "status": "success/error",
    "message": "message"
  }
  """
  req_json = request.json
  if "uid" not in req_json:
    return {"status": "error", "message": "uid not found in request"}
  
  if "desired_role_id" not in req_json:
    return {"status": "error", "message": "desired_role_id not found in request"}
  
  cu = _request_ctx_stack.top.current_user
  editor_id = cu['sub']

  # get the request sender role and check if aac
  is_aac = current_app.config['auth0_web_api'].user_has_role(editor_id, "aac", "impossible_role_id")

  if not is_aac:
    return {"status": "error", "message": "Only AACs can manage roles"}
  
  # add the users new role
  target_uid = req_json["uid"]
  target_role = req_json["desired_role_id"]

  result = current_app.config['auth0_web_api'].remove_user_role(target_uid, target_role)

  if result == 204:
    return {"status": "success", "message": "role removed"}
  else:
    return {"status": "error", "message": "role not added, status code: {}".format(result)}


@users_bp.route('/user_info', methods=['POST'])
@requires_auth
def user_info():
  """
  Endpoint: /users/user_info
  Method: POST
  Description: Returns a user's info. Sender must be an AAC.

  Request format:
  { "uid": "target user_id" }

  Response format:
  {
    "status": "success/error",
    "user_info": {}
  }
  """
  req_json = request.json

  if "uid" not in req_json:
    return {"status": "error", "message": "uid not found in request"}
  
  cu = _request_ctx_stack.top.current_user
  editor_id = cu['sub']

  # get the request sender role and check if aac
  is_aac = current_app.config['auth0_web_api'].user_has_role(editor_id, "aac", "impossible_role_id")

  if not is_aac:
    return {"status": "error", "message": "Only AACs can view user info"}
  
  # add the users new role
  target_uid = req_json["uid"]

  status, result = current_app.config['auth0_web_api'].get_user_info(target_uid)

  if status == 200:
    return {"status": "success", "user_info": result}

  return {"status": "error", "message": "user info not found, status code: {}".format(status)}


@users_bp.route('/get_user_roles', methods=['POST'])
@requires_auth
def user_roles():
  """
  Endpoint: /users/get_user_roles
  Method: POST
  Description: Returns a user's roles. Sender must be an AAC.

  Request format:
  { "uid": "target user_id" }

  Response format:
  {
    "status": "success/error",
    "user_info": {}
  }
  """
  req_json = request.json

  if "uid" not in req_json:
    return {"status": "error", "message": "uid not found in request"}
  
  cu = _request_ctx_stack.top.current_user
  editor_id = cu['sub']

  # get the request sender role and check if aac
  is_aac = current_app.config['auth0_web_api'].user_has_role(editor_id, "aac", "impossible_role_id")

  if not is_aac:
    return {"status": "error", "message": "Only AACs can view user info"}
  
  # add the users new role
  target_uid = req_json["uid"]

  status, result = current_app.config['auth0_web_api'].get_user_roles(target_uid)

  if status == 200:
    return {"status": "success", "user_roles": result}

  return {"status": "error", "message": "user info not found, status code: {}".format(status)}







