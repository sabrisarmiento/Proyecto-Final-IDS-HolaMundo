from flask import Blueprint, request
from services.student_service import (
    students_service,
    student_service,
    create_student_service,
    import_students_service,
    update_student_service
)
from middleware.auth_middleware import require_auth, require_min_admin_level
from helpers.constants import NIVEL_PROFESOR

students_bp = Blueprint('students', __name__)


@students_bp.route("/students", methods=["GET"])
@require_auth
def get_students():
    per_page = request.args.get('per_page', 10, type=int)
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * per_page

    filters = {
        "nombre": request.args.get('nombre'),
        "apellido": request.args.get('apellido'),
        "padron": request.args.get('padron'),
        "mail": request.args.get('mail'),
        "password": request.args.get('password'),
        "id_rol": request.args.get('id_rol'),
        "created_at": request.args.get('created_at'),
        "id_curso": request.args.get('id_curso'),
        "limit": per_page,
        "offset": offset,
        "order_by": request.args.get('order_by'),
        "order": request.args.get('order')
    }
    return students_service(filters)


@students_bp.route("/students/<int:id>", methods=["GET"])
@require_auth
def get_student(id):
    return student_service(id)


@students_bp.route("/students", methods=["POST"])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def create_student_route():
    return create_student_service(request.get_json(silent=True), request.user)


@students_bp.route("/students/import", methods=["POST"])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def import_students_route():
    id_curso = request.form.get("id_curso") or request.args.get("id_curso")
    return import_students_service(request.files, id_curso, request.user)

@students_bp.route("/students/<int:id>", methods=["PATCH"])
@require_auth
@require_min_admin_level(NIVEL_PROFESOR)
def update_student_route(id):
    return update_student_service(id, request.get_json(silent=True), request.user)