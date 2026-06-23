from flask import Blueprint, request
from services.slack_service import configure_slack_course_service, get_slack_messages_service, disconnect_slack_service
from middleware.auth_middleware import require_auth, require_min_admin_level
from helpers.constants import NIVEL_PROFESOR

slack_bp = Blueprint("slack", __name__)

@slack_bp.route("/courses/<int:id_curso>/slack/config", methods=["POST"])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def configure_slack(id_curso):
    data = request.get_json()
    return configure_slack_course_service(id_curso, data, request.user)


@slack_bp.route("/courses/<int:id_curso>/slack/messages", methods=["GET"])
@require_auth
def get_slack_messages(id_curso):
    return get_slack_messages_service(id_curso)


@slack_bp.route("/courses/<int:id_curso>/slack/disconnect", methods=["DELETE"])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def disconnect_slack(id_curso):
    return disconnect_slack_service(id_curso, request.user)