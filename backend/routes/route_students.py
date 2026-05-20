from flask import Blueprint, request
from handlers.students_handler import (
    handle_list_students,
    handle_search_student_by_id,
    handle_create_student,
    handle_import_students,
)

students_bp = Blueprint('students', __name__)

@students_bp.route("/students", methods=["GET"])
def list_students_route():
    filters = {
        "name": request.args.get("nombre"),
        "surname": request.args.get("apellido"),
        "mail": request.args.get("mail"),
        "password": request.args.get("password"),
        "id_rol": request.args.get("id_rol"),
        "created_at": request.args.get("created_at"),
    }
    return handle_list_students(filters)

@students_bp.route("/students/<int:id>", methods=["GET"])
def search_student_route(id):
    return handle_search_student_by_id(id)

@students_bp.route("/students", methods=["POST"])
def create_student_route():
    return handle_create_student(request.get_json(silent=True))

@students_bp.route("/students/import", methods=["POST"])
def import_students_route():
    return handle_import_students(request.files)