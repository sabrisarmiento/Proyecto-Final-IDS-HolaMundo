from flask import Blueprint, request
from services.subject_service import (
  subjects_service,
  subject_service,
  create_subject_service
)
from middleware.auth_middleware import require_auth

subjects_bp = Blueprint('subjects', __name__)

@subjects_bp.route('/subjects', methods=['GET'])
def get_subjects():

  filters = {
    "name" : request.args.get('nombre')
  }

  return subjects_service(filters)

@subjects_bp.route('/subjects/<int:subject_id>', methods=['GET'])
def get_subject(subject_id):
  return subject_service(subject_id)

@subjects_bp.route('/subjects', methods=['POST'])
@require_auth
def create_subject():
  data = request.get_json()
  return create_subject_service(data)