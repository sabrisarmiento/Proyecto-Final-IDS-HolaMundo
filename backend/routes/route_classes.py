from flask import Blueprint
from handlers.classes_handler import classes_handler, class_get_handler, class_post_handler, class_patch_handler, delete_class_handler

classes_bp = Blueprint('classes', __name__)

@classes_bp.route('/clases', methods=['GET'])
def get_classes():
    return classes_handler()
  
@classes_bp.route('/clases/<int:id>', methods=['GET'])
def get_class_id(id_clase):
    return class_get_handler(id_clase)

@classes_bp.route('/clases', methods=['POST'])
def add_class():
    return class_post_handler()

@classes_bp.route('/clases/<int:id>', methods=['PATCH'])
def edit_class(id_clase):
    return class_patch_handler(id_clase)

@classes_bp.route('/clases/<int:id>', methods=['DELETE'])
def remove_class(id):
    return delete_class_handler(id)