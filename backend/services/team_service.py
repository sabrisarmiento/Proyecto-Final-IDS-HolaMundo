from helpers.responses import error_response, success_response
from controllers.teams_controller import get_all_teams, get_team_by_id, create_team, patch_team_by_id, delete_team_by_id

def teams_service(filters):
    result = get_all_teams(filters)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "teams": result["data"]
    })

def team_service(id_team):
    result = get_team_by_id(id_team)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "team": result["data"]
    })

def create_team_service(data):
    result = create_team(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": "Equipo creado correctamente",
        "id_equipo": result["id_equipo"]
    }, 201)

def patch_team_service(id_team, data):
    result = patch_team_by_id(id_team, data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })

def delete_team_service(id_team):
    result = delete_team_by_id(id_team)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })