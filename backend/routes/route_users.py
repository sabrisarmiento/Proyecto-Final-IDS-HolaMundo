from flask import Blueprint
from controller.users_controller import (list_users, get_user, create_user, update_user, delete_user)

users_bp = Blueprint('users', __name__)
@users_bp.route("/usuarios",methods=["GET"])

def get_users():

    id_usuario = request.args.get("id_usuario")
    nombre = request.args.get("nombre")
    apellido = request.args.get("apellido")
    correo = request.args.get("correo")
    created_at = request.args.get("created_at")
    id_rol = request.args.get("id_rol")
    
    return list_users(id_usuario, nombre, apellido, correo, created_at, id_rol)

@users_bp.route("/usuarios/<int:id_usuario>",methods=["GET"])
def get_user_route(id_usuario):
    return get_user(id_usuario)

@users_bp.route("/usuarios",methods=["POST"])
def create_user_route():
    data = request.get_json()
    return create_user(data)

@users_bp.route("/usuarios/<int:id_usuario>",methods=["PATCH"])
def update_user_route(id_usuario):
    data = request.get_json()
    return update_user(id_usuario,data)

@users_bp.route("/usuarios/<int:id_usuario>",methods=["DELETE"])
def delete_user_route(id_usuario):
    return delete_user(id_usuario)
