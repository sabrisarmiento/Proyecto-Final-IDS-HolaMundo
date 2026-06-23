from flask import Blueprint, request
from services.class_service import (
    class_service, 
    class_get_service, 
    create_class_service, 
    update_class_service, 
    delete_class_service,
    classes_by_subject_service
)
from middleware.auth_middleware import require_auth, require_min_admin_level
from helpers.constants import NIVEL_PROFESOR

classes_bp = Blueprint('classes', __name__)

@classes_bp.route('/clases', methods=['GET'])
def get_classes_route():
    filters = {
        "fecha": request.args.get("fecha"),
        "id_curso": request.args.get("id_curso")
    }
    return class_service(filters)

@classes_bp.route('/clases/<int:id_clase>', methods=['GET'])
def get_class_id_route(id_clase):
    return class_get_service(id_clase)

@classes_bp.route('/clases/materia/<int:id_subject>', methods=['GET'])
def get_classes_by_subject_route(id_subject):
    return classes_by_subject_service(id_subject)


@classes_bp.route('/clases', methods=['POST'])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def create_class_route():
    data = request.get_json()
    return create_class_service(data, request.user)

@classes_bp.route('/clases/<int:id_clase>', methods=['PATCH'])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def update_class_route(id_clase):
    data = request.get_json()
    return update_class_service(id_clase, data, request.user)


@classes_bp.route('/clases/<int:id_clase>', methods=['DELETE'])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def delete_class_route(id_clase):
    return delete_class_service(id_clase, request.user)

