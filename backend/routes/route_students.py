from flask import Blueprint, request
from services.student_service import (
    students_service,
    student_service,
    create_student_service,
    import_students_service,
)
from middleware.auth_middleware import require_auth

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
def create_student_route():
    return create_student_service(request.get_json(silent=True))


@students_bp.route("/students/import", methods=["POST"])
@require_auth
def import_students_route():
    return import_students_service(request.files)