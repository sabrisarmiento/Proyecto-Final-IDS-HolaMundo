from flask import Blueprint, request
from services.slack_service import install_slack_service, slack_oauth_callback_service, disconnect_slack_service
from middleware.auth_middleware import require_auth

slack_bp = Blueprint("slack", __name__)


@slack_bp.route("/slack/install/<int:id_curso>", methods=["GET"])
@require_auth
def install_slack(id_curso):
    return install_slack_service(id_curso, request.user)


@slack_bp.route("/slack/oauth/callback", methods=["GET"])
def slack_oauth_callback():
    code = request.args.get("code")
    state = request.args.get("state")
    error = request.args.get("error")

    return slack_oauth_callback_service(code, state, error)

@slack_bp.route("/slack/disconnect/<int:id_curso>", methods=["DELETE"])
@require_auth
def disconnect_slack(id_curso):
    return disconnect_slack_service(id_curso)