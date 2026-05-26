from flask import Blueprint, request
from services.material_service import (
    materials_service,
    create_material_service,
    delete_material_service
)
from middleware.auth_middleware import require_auth

materials_bp = Blueprint('materials', __name__)

@materials_bp.route('/materials', methods=['GET'])
def get_materials_route():

    filters = {
        "id_curso": request.args.get('id_curso'),
        "titulo": request.args.get('titulo')
    }

    return materials_service(filters)


@materials_bp.route('/materials', methods=['POST'])
@requiere_auth
def create_material_route():
    data = request.get_json()
    return create_material_service(data)


@materials_bp.route('/materials/<int:id_material>', methods=['DELETE'])
@requiere_auth
def delete_material_route(id_material):
    return delete_material_service(id_material)