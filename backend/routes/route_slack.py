from flask import Blueprint, request
from services.slack_service import configure_slack_course_service, get_slack_messages_service, disconnect_slack_service
from middleware.auth_middleware import require_auth

slack_bp = Blueprint("slack", __name__)


# @slack_bp.route("/slack/install/<int:id_curso>", methods=["GET"])
# @require_auth
# def install_slack(id_curso):
#     return install_slack_service(id_curso, request.user)


# @slack_bp.route("/slack/oauth/callback", methods=["GET"])
# def slack_oauth_callback():
#     code = request.args.get("code")
#     state = request.args.get("state")
#     error = request.args.get("error")

#     return slack_oauth_callback_service(code, state, error)
@slack_bp.route("/courses/<int:id_curso>/slack/config", methods=["POST"])
@require_auth
def configure_slack(id_curso):
    data = request.get_json()
    return configure_slack_course_service(id_curso, data, request.user)


@slack_bp.route("/courses/<int:id_curso>/slack/messages", methods=["GET"])
def get_slack_messages(id_curso):
    return get_slack_messages_service(id_curso)


@slack_bp.route("/courses/<int:id_curso>/slack/disconnect", methods=["DELETE"])
#@slack_bp.route("/slack/disconnect/<int:id_curso>", methods=["DELETE"])
@require_auth
def disconnect_slack(id_curso):
    return disconnect_slack_service(id_curso)