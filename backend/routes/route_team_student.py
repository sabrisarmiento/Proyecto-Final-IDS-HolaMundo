from flask import Blueprint, request
from services.team_student_service import add_student_to_team_service, remove_student_from_team_service
from middleware.auth_middleware import require_auth, require_min_admin_level
from helpers.constants import NIVEL_PROFESOR

team_student_bp = Blueprint("team_student", __name__)
@team_student_bp.route("/equipo-alumno", methods=["POST"])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def add_student_team_route():
    data = request.get_json()
    return add_student_to_team_service(data, request.user)

@team_student_bp.route("/equipo-alumno", methods=["DELETE"])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def remove_student():
    data = request.get_json()
    return remove_student_from_team_service(data, request.user)