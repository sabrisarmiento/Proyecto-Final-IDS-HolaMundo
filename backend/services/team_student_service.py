from helpers.responses import error_response, success_response
from helpers.user_belongs import user_can_manage_equipo
from controllers.team_student_controller import add_student_to_team, remove_student_from_team

def add_student_to_team_service(data, user):
    if not user_can_manage_equipo((data or {}).get("id_equipo"), user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre este equipo"
        })
    result = add_student_to_team(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })

def remove_student_from_team_service(data, user):
    if not user_can_manage_equipo((data or {}).get("id_equipo"), user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre este equipo"
        })
    result = remove_student_from_team(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })