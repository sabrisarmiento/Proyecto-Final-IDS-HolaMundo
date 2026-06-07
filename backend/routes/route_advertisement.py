from flask import Blueprint, request
from services.advertisement_service import (
    advertisements_service,
    advertisement_service,
    create_advertisement_service,
    patch_advertisement_service,
    delete_advertisement_service,
    advertisements_by_subject_service,
)
from services.slack_advertisement_service import slack_advertisements_service
from middleware.auth_middleware import require_auth
from helpers.logger import log_action

advertisements_bp = Blueprint('advertisements', __name__)


def _user_info(req):
    """Devuelve (id_usuario, nombre) del token si existe."""
    user = getattr(req, "user", {}) or {}
    nombre = f"{user.get('nombre', '')} {user.get('apellido', '')}".strip()
    return user.get("id_usuario"), nombre or user.get("correo", "Desconocido")

@advertisements_bp.route('/advertisements', methods=['GET'])
def get_advertisements():
    filters = {
        "id_usuario": request.args.get('id_usuario'),
        "id_curso":   request.args.get('id_curso'),
        "titulo":     request.args.get('titulo'),
        "fecha":      request.args.get('fecha'),
    }
    return advertisements_service(filters)

@advertisements_bp.route('/advertisements/slack', methods=['GET'])
def get_slack_advertisements_route():
    result = slack_advertisements_service()

    id_u, nombre_u = _user_info(request)
    log_action(
        accion="CONSULTA_SLACK",
        descripcion="Se consultaron los avisos del canal de Slack",
        id_usuario=id_u,
        nombre_usuario=nombre_u if id_u else "Visitante",
    )

    return result

@advertisements_bp.route('/advertisements/<id_advertisement>', methods=['GET'])
def get_advertisement_by_id_route(id_advertisement):
    return advertisement_service(id_advertisement)

@advertisements_bp.route('/advertisements', methods=['POST'])
@require_auth
def create_advertisement():
    data = request.get_json()
    result = create_advertisement_service(data, request.user)

    if result[1] == 201:
        id_u, nombre_u = _user_info(request)
        id_curso = data.get("id_curso") if data else None
        titulo   = data.get("titulo", "sin título") if data else "sin título"
        log_action(
            accion="CREAR_AVISO",
            descripcion=f"Se publicó el aviso \"{titulo}\"",
            id_usuario=id_u,
            nombre_usuario=nombre_u,
            id_curso=id_curso,
        )

    return result

@advertisements_bp.route('/advertisements/<id_advertisement>', methods=['PATCH'])
@require_auth
def update_advertisement(id_advertisement):
    data = request.get_json()
    result = patch_advertisement_service(id_advertisement, data)

    if result[1] == 200:
        id_u, nombre_u = _user_info(request)
        log_action(
            accion="EDITAR_AVISO",
            descripcion=f"Se editó el aviso ID {id_advertisement}",
            id_usuario=id_u,
            nombre_usuario=nombre_u,
        )

    return result

@advertisements_bp.route('/advertisements/<id_advertisement>', methods=['DELETE'])
@require_auth
def delete_advertisement(id_advertisement):
    result = delete_advertisement_service(id_advertisement)

    if result[1] == 200:
        id_u, nombre_u = _user_info(request)
        log_action(
            accion="ELIMINAR_AVISO",
            descripcion=f"Se eliminó el aviso ID {id_advertisement}",
            id_usuario=id_u,
            nombre_usuario=nombre_u,
        )

    return result

@advertisements_bp.route('/advertisements/subject/<int:id_materia>', methods=['GET'])
def get_advertisements_by_subject_route(id_materia):
    return advertisements_by_subject_service(id_materia)