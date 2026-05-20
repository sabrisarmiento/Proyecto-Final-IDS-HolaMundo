from flask import Blueprint

from handlers.team_handler import get_team_handler, get_team_by_id_handler, get_team_by_members_handler, create_team_handler, update_team_handler, delete_team_handler

teams_bp = Blueprint("teams", __name__)

@teams_bp.route("/equipos", methods=["GET"])
def get_teams():
    return get_team_handler()

@teams_bp.route("/equipos/<int:id>", methods=["GET"])
def get_team_by_id(id):
    return get_team_by_id_handler(id)

@teams_bp.route("/equipos/integrante/<int:id_usuario>", methods=["GET"])
def get_team_by_members(id_usuario):
    return get_team_by_members_handler(id_usuario)

@teams_bp.route("/equipos", methods=["POST"])
def create_team():
    return create_team_handler()

@teams_bp.route("/equipos/<int:id>", methods=["PATCH"])
def update_team(id):
    return update_team_handler(id)

@teams_bp.route("/equipos/<int:id>", methods=["DELETE"])
def delete_team(id):
    return delete_team_handler(id)