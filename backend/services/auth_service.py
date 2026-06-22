from controllers.auth_controller import login_user, change_password
from controllers.users_controller import get_user_by_id
from helpers.responses import error_response, success_response

def login_service(data):
    result = login_user(data)
    if not result["ok"]:
        return error_response(result)

    return success_response({
        "message": result["message"],
        "token": result["token"],
        "user": result["user"]
    })

def me_service(user):
    id_usuario = user["id_usuario"]
    result = get_user_by_id(id_usuario)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "user": result["data"]
    })

def change_password_service(data, id_usuario):
    result = change_password(data, id_usuario)

    if not result["ok"]:
        return error_response(result)

    return success_response({
        "message": result["message"]
    })