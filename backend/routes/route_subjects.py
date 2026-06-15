from flask import Blueprint, request
from services.subject_service import (
  subjects_service,
  subject_service,
  get_topics_service,
  create_subject_service,
  patch_subject_service,
  delete_subject_service,
  my_subjects_service
)
from middleware.auth_middleware import require_auth

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

@subjects_bp.route('/subjects', methods=['POST'])
@require_auth
def create_subject():
  data = request.get_json()
  return create_subject_service(data)

@subjects_bp.route('/subjects/<int:subject_id>', methods=['PATCH'])
@require_auth
def patch_subject(subject_id):
  data = request.get_json()
  return patch_subject_service(subject_id, data)

@subjects_bp.route('/subjects/<int:subject_id>', methods=['DELETE'])
@require_auth
def delete_subject(subject_id):
  return delete_subject_service(subject_id)