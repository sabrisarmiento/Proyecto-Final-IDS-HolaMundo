from flask import Blueprint, request
from services.courses_service import (
    courses_service,
    course_service,
    create_course_service,
    patch_course_service,
    delete_course_service
)
from middleware.auth_middleware import require_auth

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/courses', methods=['GET'])
def get_courses():
    filters = {
        "nombre": request.args.get('nombre'),
        "cuatrimestre": request.args.get('cuatrimestre'),
        "anio": request.args.get('anio')
    }
    return courses_service(filters)

@courses_bp.route('/courses/<int:id_course>', methods=['GET'])
def get_course(id_course):
    return course_service(id_course)

@courses_bp.route('/courses', methods=['POST'])
@require_auth
def create_course_route():
    data = request.get_json()
    return create_course_service(data)

@courses_bp.route('/courses/<int:id_course>', methods=['PATCH'])
@require_auth
def patch_course_route(id_course):
    data = request.get_json()
    return patch_course_service(id_course, data)

@courses_bp.route('/courses/<int:id_course>', methods=['DELETE'])
@require_auth
def delete_course_route(id_course):
    return delete_course_service(id_course)