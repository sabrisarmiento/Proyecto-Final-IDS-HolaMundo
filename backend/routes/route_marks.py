from flask import Blueprint
from handlers.marks_handler import (
    marks_handler,
    mark_handler,
    create_mark_handler,
    patch_mark_handler,
    delete_mark_handler
)

marks_bp = Blueprint('marks', __name__)

@marks_bp.route('/marks', methods=['GET'])
def get_marks():
    return marks_handler()


@marks_bp.route('/marks/<int:id_mark>', methods=['GET'])
def get_mark(id_mark):
    return mark_handler(id_mark)


@marks_bp.route('/marks', methods=['POST'])
def create_mark():
    return create_mark_handler()


@marks_bp.route('/marks/<int:id_mark>', methods=['PATCH'])
def patch_mark(id_mark):
    return patch_mark_handler(id_mark)


@marks_bp.route('/marks/<int:id_mark>', methods=['DELETE'])
def delete_mark(id_mark):
    return delete_mark_handler(id_mark)
