from flask import Blueprint, request
from services.team_student_service import add_student_to_team_service

team_student_bp = Blueprint("team_student", __name__)
@team_student_bp.route("/equipo-alumno", methods=["POST"])
def add_student_team_route():
    data = request.get_json()
    return add_student_to_team_service(data)