from flask import Blueprint

from services.team_service import teams_service, team_service, create_team_service, patch_team_service, delete_team_service

teams_bp = Blueprint("teams", __name__)

@teams_bp.route("/equipos", methods=["GET"])
def get_teams():
    filters = {
        "id_alumno": request.args.get("id_alumno"),
        "id_curso": request.args.get("id_curso")
    }
    return teams_service(filters)

@teams_bp.route("/equipos/<int:id_team>", methods=["GET"])
def get_team(id_team):
    return team_service(id_team)

@teams_bp.route("/equipos", methods=["POST"])
def create_team():
    data = request.get_json()
    return create_team_service(data)

@teams_bp.route("/equipos/<int:id_team>", methods=["PATCH"])
def update_team(id_team):
    data = request.get_json()
    return patch_team_service(id_team, data)

@teams_bp.route("/equipos/<int:id_team>", methods=["DELETE"])
def delete_team(id_team):
    return delete_team_service(id_team)