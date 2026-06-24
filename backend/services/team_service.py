from helpers.responses import error_response, success_response
from helpers.user_belongs import user_can_manage_course, user_can_manage_equipo
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

def create_team_service(data, user):
    if not user_can_manage_course((data or {}).get("id_curso"), user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre este curso"
        })
    result = create_team(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": "Equipo creado correctamente",
        "id_equipo": result["id_equipo"]
    }, 201)

def patch_team_service(id_team, data, user):
    if not user_can_manage_equipo(id_team, user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre este equipo"
        })
    result = patch_team_by_id(id_team, data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })

def delete_team_service(id_team, user):
    if not user_can_manage_equipo(id_team, user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre este equipo"
        })
    result = delete_team_by_id(id_team)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })