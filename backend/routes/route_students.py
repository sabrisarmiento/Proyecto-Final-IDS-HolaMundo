from flask import Blueprint, request
from services.student_service import (
    fetch_students_service,
    fetch_student_id_service,
    create_student_service,
    import_students_service,
)
from middleware.auth_middleware import require_auth

students_bp = Blueprint('students', __name__)


@students_bp.route("/students", methods=["GET"])
@requiere_auth
def get_students():
    filters = {
        "nombre": request.args.get('nombre'),
        "apellido": request.args.get('apellido'),
        "mail": request.args.get('mail'),
        "password": request.args.get('password'),
        "id_rol": request.args.get('id_rol'),
        "created_at": request.args.get('created_at'),
    }
    return fetch_students_service(filters)


@students_bp.route("/students/<int:id>", methods=["GET"])
@requiere_auth
def get_student(id):
    return fetch_student_id_service(id)


@students_bp.route("/students", methods=["POST"])
@requiere_auth
def create_student_route():
    return create_student_service(request.get_json(silent=True))


@students_bp.route("/students/import", methods=["POST"])
@requiere_auth
def import_students_route():
    return import_students_service(request.files)