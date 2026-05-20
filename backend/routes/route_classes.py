from flask import Blueprint
from handlers.classes_handler import classes_get_handler, class_get_handler, class_post_handler, class_patch_handler

classes_bp = Blueprint('classes', __name__)

@classes_bp.route('/clases', methods=['GET'])
def get_classes():
    return classes_get_handler()
  
@classes_bp.route('/clases/<int:id>', methods=['GET'])
def get_class_by_id(id):
    return class_get_handler(id)

@classes_bp.route('/clases', methods=['POST'])
def add_class():
    return class_post_handler()

@classes_bp.route('/clases/<int:id>', methods=['PATCH'])
def edit_class(id):
    return class_patch_handler(id)