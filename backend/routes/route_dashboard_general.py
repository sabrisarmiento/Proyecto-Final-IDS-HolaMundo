from flask import Blueprint, request
from helpers.responses import error_response, success_response
from controllers.dashboard_general_controller import get_general_dashboard
from controllers.logs_controller import get_logs
from controllers.users_controller import create_user, update_user_by_id, delete_user_by_id
from controllers.roles_controller import create_rol, delete_rol_by_id
from middleware.auth_middleware import require_auth
from helpers.logger import log_action

dashboard_general_bp = Blueprint('dashboard_general', __name__)

def _nombre_usuario(user):
    nombre = f"{user.get('nombre', '')} {user.get('apellido', '')}".strip()
    return nombre or user.get("correo", "Desconocido")

@dashboard_general_bp.route('/dashboard/general', methods=['GET'])
# @require_auth descomentar cuanto este listo
def get_dashboard_general():
    result = get_general_dashboard()
    if not result["ok"]:
        return error_response(result)
    return success_response(result["data"])

@dashboard_general_bp.route('/dashboard/logs', methods=['GET'])
# @require_auth descomentar cuanto este listo
def get_logs_route():
    result = get_logs(
        limit=request.args.get('limit', 100),
        id_usuario=request.args.get('id_usuario'),
        id_curso=request.args.get('id_curso'),
        accion=request.args.get('accion'),
    )
    if not result["ok"]:
        return error_response(result)
    return success_response({"logs": result["data"]})

@dashboard_general_bp.route('/dashboard/usuarios', methods=['POST'])
# @require_auth descomentar cuanto este listo
def crear_usuario_dashboard():
    data = request.get_json(silent=True)
    result = create_user(data)
    if not result["ok"]:
        return error_response(result)
    user = request.user
    log_action(
        accion="CREAR_USUARIO",
        descripcion=f"Se creó el usuario {data.get('nombre')} {data.get('apellido')} ({data.get('correo')})",
        id_usuario=user.get("id_usuario"),
        nombre_usuario=_nombre_usuario(user),
    )
    return success_response({"message": result["message"]}, 201)


@dashboard_general_bp.route('/dashboard/usuarios/<int:id_user>', methods=['PATCH'])
# @require_auth descomentar cuanto este listo
def actualizar_usuario_dashboard(id_user):
    data = request.get_json(silent=True)
    result = update_user_by_id(id_user, data)
    if not result["ok"]:
        return error_response(result)
    user = request.user
    log_action(
        accion="EDITAR_USUARIO",
        descripcion=f"Se modificó el usuario ID {id_user} (nuevos datos: {data})",
        id_usuario=user.get("id_usuario"),
        nombre_usuario=_nombre_usuario(user),
    )
    return success_response({"message": result["message"]})


@dashboard_general_bp.route('/dashboard/usuarios/<int:id_user>', methods=['DELETE'])
# @require_auth descomentar cuanto este listo
def eliminar_usuario_dashboard(id_user):
    result = delete_user_by_id(id_user)
    if not result["ok"]:
        return error_response(result)
    user = request.user
    log_action(
        accion="ELIMINAR_USUARIO",
        descripcion=f"Se eliminó el usuario ID {id_user}",
        id_usuario=user.get("id_usuario"),
        nombre_usuario=_nombre_usuario(user),
    )
    return success_response({"message": result["message"]})

@dashboard_general_bp.route('/dashboard/roles', methods=['POST'])
# @require_auth descomentar cuanto este listo
def crear_rol_dashboard():
    data = request.get_json(silent=True)
    result = create_rol(data)
    if not result["ok"]:
        return error_response(result)
    user = request.user
    log_action(
        accion="CREAR_ROL",
        descripcion=f"Se creó el rol \"{data.get('nombre')}\" (nivel {data.get('nivel_administracion')})",
        id_usuario=user.get("id_usuario"),
        nombre_usuario=_nombre_usuario(user),
    )
    return success_response({"message": result["message"], "id": result["id"]}, 201)


@dashboard_general_bp.route('/dashboard/roles/<int:id_rol>', methods=['DELETE'])
# @require_auth descomentar cuanto este listo
def eliminar_rol_dashboard(id_rol):
    result = delete_rol_by_id(id_rol)
    if not result["ok"]:
        return error_response(result)
    user = request.user
    log_action(
        accion="ELIMINAR_ROL",
        descripcion=f"Se eliminó el rol ID {id_rol}",
        id_usuario=user.get("id_usuario"),
        nombre_usuario=_nombre_usuario(user),
    )
    return success_response({"message": "Rol eliminado correctamente"})