from flask import Blueprint, request
from services.subject_service import (
  subjects_service,
  subject_service,
  get_topics_service,
  replace_temas_service,
  create_subject_service,
  patch_subject_service,
  delete_subject_service,
  my_subjects_service,
  get_professors_by_subject_service,
  assign_professor_to_subject_service,
  remove_professor_from_subject_service,
  get_subjects_assigned_to_professor_service
)
from middleware.auth_middleware import require_auth, require_min_admin_level
from helpers.constants import NIVEL_SUPERADMIN, NIVEL_PROFESOR

subjects_bp = Blueprint('subjects', __name__)

@subjects_bp.route('/subjects', methods=['GET'])
def get_subjects():
  filters = {
    "name" : request.args.get('nombre')
  }
  return subjects_service(filters)

@subjects_bp.route('/subjects/mias', methods=['GET'])
@require_auth
def get_my_subjects():
    user = request.user
    is_admin = (user.get("nivel") or 0) >= 3
    filters = {"name": request.args.get('nombre')}
    return my_subjects_service(user["id_usuario"], is_admin, filters)


@subjects_bp.route('/subjects/<int:subject_id>', methods=['GET'])
def get_subject(subject_id):
  return subject_service(subject_id)

@subjects_bp.route('/subjects/<int:subject_id>/temas', methods=['GET'])
def get_subject_topics(subject_id):
    return get_topics_service(subject_id)

@subjects_bp.route('/subjects/<int:subject_id>/temas', methods=['PUT'])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def replace_subject_topics(subject_id):
    data = request.get_json()
    temas = data.get("temas", []) if data else []
    return replace_temas_service(subject_id, temas)

@subjects_bp.route('/subjects', methods=['POST'])
@require_auth
@require_min_admin_level(NIVEL_SUPERADMIN)
def create_subject():
  data = request.get_json()
  return create_subject_service(data)

@subjects_bp.route('/subjects/<int:subject_id>', methods=['PATCH'])
@require_auth
@require_min_admin_level(NIVEL_SUPERADMIN)
def patch_subject(subject_id):
  data = request.get_json()
  return patch_subject_service(subject_id, data)

@subjects_bp.route('/subjects/<int:subject_id>', methods=['DELETE'])
@require_auth
@require_min_admin_level(NIVEL_SUPERADMIN)
def delete_subject(subject_id):
  return delete_subject_service(subject_id)

@subjects_bp.route("/subjects/<int:id_materia>/professors", methods=["GET"])
@require_auth
@require_min_admin_level(NIVEL_SUPERADMIN)
def get_subject_professors_route(id_materia):
    return get_professors_by_subject_service(id_materia)

@subjects_bp.route("/subjects/<int:id_materia>/professors", methods=["POST"])
@require_auth
@require_min_admin_level(NIVEL_SUPERADMIN)
def assign_professor_to_subject_route(id_materia):
    data = request.get_json()
    return assign_professor_to_subject_service(id_materia, data)

@subjects_bp.route("/subjects/<int:id_materia>/professors/<int:id_profesor>", methods=["DELETE"])
@require_auth
@require_min_admin_level(NIVEL_SUPERADMIN)
def remove_professor_from_subject_route(id_materia, id_profesor):
    return remove_professor_from_subject_service(id_materia, id_profesor)

@subjects_bp.route("/subjects/my-assigned", methods=["GET"])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def get_my_assigned_subjects_route():
    id_profesor = request.user["id_usuario"]

    return get_subjects_assigned_to_professor_service(id_profesor)