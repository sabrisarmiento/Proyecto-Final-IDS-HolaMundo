from flask import Blueprint, request
from helpers.responses import error_response, success_response
from controllers.dashboard_general_controller import get_general_dashboard
from controllers.users_controller import create_user, update_user_by_id, delete_user_by_id
from controllers.roles_controller import create_rol, delete_rol_by_id
from middleware.auth_middleware import require_auth

dashboard_general_bp = Blueprint('dashboard_general', __name__)


@dashboard_general_bp.route('/dashboard/general', methods=['GET'])
@require_auth
def get_dashboard_general():
    result = get_general_dashboard()
    if not result["ok"]:
        return error_response(result)
    return success_response(result["data"])

@dashboard_general_bp.route('/dashboard/usuarios', methods=['POST'])
@require_auth
def crear_usuario_dashboard():
    data = request.get_json(silent=True)
    logged_user = request.user
    result = create_user(data, logged_user)
    if not result["ok"]:
        return error_response(result)
    return success_response({"message": result["message"]}, 201)


@dashboard_general_bp.route('/dashboard/usuarios/<int:id_user>', methods=['PATCH'])
@require_auth
def actualizar_usuario_dashboard(id_user):
    data = request.get_json(silent=True)
    logged_user = request.user
    result = update_user_by_id(id_user, data, logged_user)
    if not result["ok"]:
        return error_response(result)
    return success_response({"message": result["message"]})


@dashboard_general_bp.route('/dashboard/usuarios/<int:id_user>', methods=['DELETE'])
@require_auth
def eliminar_usuario_dashboard(id_user):
    logged_user = request.user
    result = delete_user_by_id(id_user, logged_user)
    if not result["ok"]:
        return error_response(result)
    return success_response({"message": result["message"]})

@dashboard_general_bp.route('/dashboard/roles', methods=['POST'])
@require_auth
def crear_rol_dashboard():
    data = request.get_json(silent=True)
    result = create_rol(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({"message": result["message"], "id": result["id"]}, 201)


@dashboard_general_bp.route('/dashboard/roles/<int:id_rol>', methods=['DELETE'])
@require_auth
def eliminar_rol_dashboard(id_rol):
    result = delete_rol_by_id(id_rol)
    if not result["ok"]:
        return error_response(result)
    return success_response({"message": "Rol eliminado correctamente"})