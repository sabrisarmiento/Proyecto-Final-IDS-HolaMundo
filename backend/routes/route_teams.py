from flask import Blueprint, request

from services.team_service import teams_service, team_service, create_team_service, patch_team_service, delete_team_service

from middleware.auth_middleware import require_auth, require_min_admin_level
from helpers.constants import NIVEL_PROFESOR

teams_bp = Blueprint("teams", __name__)


@teams_bp.route("/equipos", methods=["GET"])
@require_auth
def get_teams():
    filters = {
        "id_alumno": request.args.get("id_alumno"),
        "id_curso": request.args.get("id_curso")
    }
    return teams_service(filters)


@teams_bp.route("/equipos/<int:id_team>", methods=["GET"])
@require_auth
def get_team(id_team):
    return team_service(id_team)


@teams_bp.route("/equipos", methods=["POST"])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def create_team():
    data = request.get_json()
    return create_team_service(data)


@teams_bp.route("/equipos/<int:id_team>", methods=["PATCH"])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def update_team(id_team):
    data = request.get_json()
    return patch_team_service(id_team, data)


@teams_bp.route("/equipos/<int:id_team>", methods=["DELETE"])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def delete_team(id_team):
    return delete_team_service(id_team)
