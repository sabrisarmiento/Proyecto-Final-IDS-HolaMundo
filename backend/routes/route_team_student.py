from flask import Blueprint, request
from services.team_student_service import add_student_to_team_service, remove_student_from_team_service
from middleware.auth_middleware import require_auth

team_student_bp = Blueprint("team_student", __name__)
@team_student_bp.route("/equipo-alumno", methods=["POST"])
@require_auth
def add_student_team_route():
    data = request.get_json()
    return add_student_to_team_service(data)

@team_student_bp.route("/equipo-alumno", methods=["DELETE"])
@require_auth
def remove_student():
    data = request.get_json()
    return remove_student_from_team_service(data)