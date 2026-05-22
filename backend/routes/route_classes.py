from flask import Blueprint, request
from services.class_service import (
    class_service, 
    class_get_service, 
    create_class_service, 
    update_class_service, 
    delete_class_service
)

classes_bp = Blueprint('classes', __name__)

@classes_bp.route('/clases', methods=['GET'])
def get_classes_route():
    filters = {
        "date": request.args.get("fecha")
    }
    return class_service(filters)
  
@classes_bp.route('/clases/<int:id_clase>', methods=['GET'])
def get_class_id_route(id_clase):
    return class_get_service(id_clase)

@classes_bp.route('/clases', methods=['POST'])
def create_class_route():
    data = request.get_json()
    return create_class_service(data)

@classes_bp.route('/clases/<int:id_clase>', methods=['PATCH'])
def update_class_route(id_clase):
    data = request.get_json()
    return update_class_service(id_clase, data)

@classes_bp.route('/clases/<int:id_clase>', methods=['DELETE'])
def delete_class_route(id_clase):
    return delete_class_service(id_clase)