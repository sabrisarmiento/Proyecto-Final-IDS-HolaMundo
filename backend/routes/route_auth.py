from flask import Blueprint, request
from services.auth_service import login_service, change_password_service
from services.user_service import get_user_by_id
from middleware.auth_middleware import require_auth

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return login_service(data)

@auth_bp.route("/me", methods=["GET"])
@require_auth
def me():
    return get_user_by_id(request.user["id_usuario"])

@auth_bp.route("/change-password", methods=["PUT"])
@require_auth
def change_password_route():
    data = request.get_json()
    id_usuario = request.user["id_usuario"]
    return change_password_service(data, id_usuario)