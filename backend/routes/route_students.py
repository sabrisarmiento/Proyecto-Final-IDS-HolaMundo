from flask import Blueprint, request, jsonify
from controller.students_controller import list_students, search_student_by_id

students_bp = Blueprint('students', __name__)

@students_bp.route("/students", methods = ["GET"])
def list_students_route():
    id_alumnos = request.args.get('id_alumnos', type = int)
    name = request.args.get('nombre')
    surname = request.args.get('apellido')
    mail = request.args.get('mail')
    password = request.args.get('password')
    id_rol = request.args.get('id_rol')
    created_at = request.args.get('created_at')

    return list_students(id_alumnos, name, surname, mail, password, id_rol, created_at)

@students_bp.route("/students/<int:id>", methods = ["GET"])
def search_student(id):
    return search_student_by_id(id)


