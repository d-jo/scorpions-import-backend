from flask import Blueprint
from flask import Flask, flash, request, redirect, url_for, current_app, _request_ctx_stack
from auth.auth import requires_auth

audit_bp = Blueprint("audit_bp", __name__)


@audit_bp.route('/file/<file_id>', methods=['GET'])
@requires_auth
def get_file_auditlog(file_id):
  """
  Endpoint: /audit/file/<file_id>
  Method: GET
  Description: Gets all the audit log entries for a file.

  URL Parameters:
  file_id: The id of the file to get the audit log for.

  Response format:
  {
    "status": "success/(no results/error)",
    "report_id": "id of the report",
    "audit_trail": [{
      "action": "action performed",
      "timestamp": "time of action",
      "editor_name": "name of editor",
      "audit_id": "id of audit log entry",
      "report_id": "id of report"
    },{}...]
  }
  """

  cu = _request_ctx_stack.top.current_user
  editor_id = cu['sub']

  # get the request sender role and check if aac
  is_aac = current_app.config['auth0_web_api'].user_has_role(editor_id, "aac", "impossible_role_id")

  if not is_aac:
    return {"status": "error", "message": "You are not authorized to access this resource."}, 403

  # get the audits for this file
  audits = current_app.config['audit_log_repo'].get_audits_for_report(file_id)

  return {
    "status": "success" if len(audits) > 0 else "no results/error",
    "report_id": file_id,
    "audit_trail": [x.to_dict() for x in audits]
  }, 200

  