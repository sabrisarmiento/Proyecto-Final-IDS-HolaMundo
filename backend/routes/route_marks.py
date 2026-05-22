from flask import Blueprint, request
from services.mark_service import (
    marks_handler,
    mark_handler,
    create_mark_handler,
    patch_mark_handler,
    delete_mark_handler
)

marks_bp = Blueprint('marks', __name__)

@marks_bp.route('/marks', methods=['GET'])
def get_marks():

    filters = {
        "id_alumno": request.args.get('id_alumno'),
        "id_evaluacion": request.args.get('id_evaluacion'),
        "id_equipo": request.args.get('id_equipo'),
        "id_corrector": request.args.get('id_corrector'),
        "nota": request.args.get('nota')
    }
    return marks_handler(filters)


@marks_bp.route('/marks/<int:id_mark>', methods=['GET'])
def get_mark(id_mark):
    return mark_handler(id_mark)


@marks_bp.route('/marks', methods=['POST'])
def create_mark():
    data = request.get_json()
    return create_mark_handler(data)


@marks_bp.route('/marks/<int:id_mark>', methods=['PATCH'])
def patch_mark(id_mark):
    data = request.get_json()
    return patch_mark_handler(id_mark, data)


@marks_bp.route('/marks/<int:id_mark>', methods=['DELETE'])
def delete_mark(id_mark):
    return delete_mark_handler(id_mark)
