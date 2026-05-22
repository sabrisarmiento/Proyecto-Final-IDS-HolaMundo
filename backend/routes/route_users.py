from flask import Blueprint
# from controller.users_controller import (list_users, get_user, create_user, update_user, delete_user)
from services.user_service import (
    users_handler,
    user_handler,
    create_user_handler,
    patch_user_handler,
    delete_user_handler
)

users_bp = Blueprint('users', __name__)

@users_bp.route("/usuarios",methods=["GET"])
def get_users():
    return users_handler()

    # id_usuario = request.args.get("id_usuario")
    # nombre = request.args.get("nombre")
    # apellido = request.args.get("apellido")
    # correo = request.args.get("correo")
    # created_at = request.args.get("created_at")
    # id_rol = request.args.get("id_rol")
    
    # return list_users(id_usuario, nombre, apellido, correo, created_at, id_rol)

@users_bp.route("/usuarios/<int:id_user>",methods=["GET"])
def get_user(id_user):
    return user_handler(id_user)
# def get_user_route(id_usuario):
#     return get_user(id_usuario)

@users_bp.route("/usuarios",methods=["POST"])
def create_user():
    return create_user_handler()
# def create_user_route():
#     data = request.get_json()
#     return create_user(data)

@users_bp.route("/usuarios/<int:id_user>",methods=["PATCH"])
def patch_user(id_user):
    return patch_user_handler(id_user)

# def update_user_route(id_usuario):
#     data = request.get_json()
#     return update_user(id_usuario,data)

@users_bp.route("/usuarios/<int:id_user>",methods=["DELETE"])
def delete_user(id_user):
    return delete_user_handler(id_user)
# def delete_user_route(id_usuario):
#     return delete_user(id_usuario)
