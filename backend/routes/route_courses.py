from flask import Blueprint, request
from services.courses_service import (
    courses_service,
    course_service,
    create_course_service,
    patch_course_service,
    delete_course_service,
    my_courses_service,
    get_assistants_by_course_service,
    assign_assistant_to_course_service,
    remove_assistant_from_course_service
)
from middleware.auth_middleware import require_auth, require_min_admin_level
from helpers.constants import NIVEL_PROFESOR

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/courses', methods=['GET'])
def get_courses():
    filters = {
        "materia": request.args.get('materia'),
        "cuatrimestre": request.args.get('cuatrimestre'),
        "anio": request.args.get('anio')
    }
    return courses_service(filters)

@courses_bp.route('/courses/mias', methods=['GET'])
@require_auth
def get_my_courses():
    user = request.user
    is_admin = (user.get("nivel") or 0) >= 3
    filters = {
        "materia": request.args.get('materia'),
        "catedra": request.args.get('catedra'),
        "anio": request.args.get('anio'),
    }
    return my_courses_service(user["id_usuario"], is_admin, filters)


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
@require_min_admin_level(NIVEL_PROFESOR)
def delete_course_route(id_course):
    return delete_course_service(id_course, request.user)

@courses_bp.route("/courses/<int:id_curso>/assistants", methods=["GET"])
@require_auth
def get_course_assistants_route(id_curso):
    return get_assistants_by_course_service(id_curso)

@courses_bp.route("/courses/<int:id_curso>/assistants", methods=["POST"])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def assign_assistant_to_course_route(id_curso):
    data = request.get_json()
    return assign_assistant_to_course_service(id_curso, data, request.user)

@courses_bp.route("/courses/<int:id_curso>/assistants/<int:id_ayudante>", methods=["DELETE"])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def remove_assistant_from_course_route(id_curso, id_ayudante):
    return remove_assistant_from_course_service(id_curso, id_ayudante, request.user)