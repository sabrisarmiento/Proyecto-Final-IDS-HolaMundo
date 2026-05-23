from flask import Blueprint, request
from services.user_service import (
    users_service,
    user_service,
    create_user_service,
    patch_user_service,
    delete_user_service
)

users_bp = Blueprint('users', __name__)

@users_bp.route("/users",methods=["GET"])
def get_users():

    filters = {
        "id_usuario": request.args.get("id_usuario"),
        "nombre": request.args.get("nombre"),
        "apellido": request.args.get("apellido"),
        "correo": request.args.get("correo"),
        "creado": request.args.get("created_at"),
        "id_rol": request.args.get("id_rol")
    }
    return users_service(filters)


@users_bp.route("/users/<int:id_user>",methods=["GET"])
def get_user(id_user):
    return user_service(id_user)

@users_bp.route("/users",methods=["POST"])
def create_user():
    data = request.get_json()
    return create_user_service(data)

@users_bp.route("/users/<int:id_user>",methods=["PATCH"])
def patch_user(id_user):
    data = request.get_json()
    return patch_user_service(id_user, data)

@users_bp.route("/users/<int:id_user>",methods=["DELETE"])
def delete_user(id_user):
    return delete_user_service(id_user)