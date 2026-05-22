from flask import Blueprint

from services.material_service import (
    materials_handler,
    create_material_handler,
    delete_material_handler
)

materials_bp = Blueprint('materials', __name__)

@materials_bp.route('/materials', methods=['GET'])
def get_materials_route():
    return materials_handler()

@materials_bp.route('/materials', methods=['POST'])
def create_material_route():
    return create_material_handler()

@materials_bp.route('/materials/<int:id_material>', methods=['DELETE'])
def delete_material_route(id_material):
    return delete_material_handler(id_material)