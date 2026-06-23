from flask import Blueprint, request
from services.user_service import (
    users_service,
    user_service,
    create_user_service,
    patch_user_service,
    delete_user_service
)

from middleware.auth_middleware import require_auth, require_min_admin_level
from helpers.constants import NIVEL_PROFESOR

users_bp = Blueprint('users', __name__)

@users_bp.route("/users",methods=["GET"])
@require_auth
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
@require_auth
def get_user(id_user):
    return user_service(id_user)

@users_bp.route("/users",methods=["POST"])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR) #lo ideal es crear una constante para ese 2, ese dos es el nivel de administracion. 
def create_user():
    data = request.get_json()
    logged_user = request.user
    return create_user_service(data, logged_user)


@users_bp.route("/users/<int:id_user>",methods=["PATCH"])
@require_auth
def patch_user(id_user):
    data = request.get_json()
    logged_user = request.user
    return patch_user_service(id_user, data, logged_user)


@users_bp.route("/users/<int:id_user>",methods=["DELETE"])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def delete_user(id_user):
    logged_user = request.user
    return delete_user_service(id_user, logged_user)