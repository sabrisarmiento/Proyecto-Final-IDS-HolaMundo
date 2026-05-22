from helpers.responses import error_response, success_response
from controllers.roles_controller import get_all_roles, create_rol, delete_rol_by_id

def roles_service(filters):
    result = get_all_roles(filters)
    if not result["ok"]:
        return error_response(result)
    if not result["data"]:
        return "", 204
    return success_response({"roles encontrados": result["data"]})

def create_rol_service(data):
    result = create_rol(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"],
        "id": result["id"],
    }, 201)


def delete_rol_service(id):
    result = delete_rol_by_id(id)
    if not result["ok"]:
        return error_response(result)
    return "", 204