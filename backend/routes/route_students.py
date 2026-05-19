from flask import Blueprint, request, jsonify
from controllers.students_controller import list_students, search_student_by_id, create_student, import_students

students_bp = Blueprint('students', __name__)

@students_bp.route("/students", methods = ["GET"])
def list_students_route():
    name = request.args.get('nombre')
    surname = request.args.get('apellido')
    mail = request.args.get('mail')
    password = request.args.get('password')
    id_rol = request.args.get('id_rol')
    created_at = request.args.get('created_at')

    return list_students(name, surname, mail, password, id_rol, created_at)

@students_bp.route("/students/<int:id>", methods = ["GET"])
def search_student(id):
    return search_student_by_id(id)

@students_bp.route("/students", methods = ["POST"])
def create_student_route():
    data = request.get_json()
    result, status = create_student(data)
    return jsonify(result), status

@students_bp.route("/students/import", methods = ["POST"])
def import_student_csv():
    return import_students(request.files)

