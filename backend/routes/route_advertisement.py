from flask import Blueprint, request
from services.advertisement_service import (
  advertisements_service,
  advertisement_service,
  create_advertisement_service,
  patch_advertisement_service,
  delete_advertisement_service,
  advertisements_by_subject_service
)
from services.slack_advertisement_service import slack_advertisements_service
from middleware.auth_middleware import require_auth

advertisements_bp = Blueprint('advertisements', __name__)

@advertisements_bp.route('/advertisements', methods=['GET'])
def get_advertisements():
  filters = {
    "id_usuario": request.args.get('id_usuario'),
    "id_curso": request.args.get('id_curso'),
    "titulo": request.args.get('titulo'),
    "fecha": request.args.get('fecha'),
  }
  return advertisements_service(filters)

@advertisements_bp.route('/advertisements/slack', methods=['GET'])
def get_slack_advertisements_route():
  return slack_advertisements_service()

@advertisements_bp.route('/advertisements/<id_advertisement>', methods=['GET'])
def get_advertisement_by_id_route(id_advertisement):
  return advertisement_service(id_advertisement)                


@advertisements_bp.route('/advertisements', methods=['POST'])
@require_auth
def create_advertisement():
  data = request.get_json()
  return create_advertisement_service(data)

@advertisements_bp.route('/advertisements/<id_advertisement>', methods=['PATCH'])
@require_auth
def update_advertisement(id_advertisement):
  data = request.get_json()
  return patch_advertisement_service(id_advertisement, data)


@advertisements_bp.route('/advertisements/<id_advertisement>', methods=['DELETE'])
@require_auth
def delete_advertisement(id_advertisement):
  return delete_advertisement_service(id_advertisement)

@advertisements_bp.route('/advertisements/subject/<int:id_materia>', methods=['GET'])
def get_advertisements_by_subject_route(id_materia):
    return advertisements_by_subject_service(id_materia)