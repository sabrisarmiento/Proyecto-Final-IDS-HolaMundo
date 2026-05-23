from flask import Blueprint, request
from services.attendance_service import (
    attendance_service,
    create_attendance_service,
    patch_attendance_service,
    delete_attendance_service,
)
from helpers.responses import error_response

attendance_bp = Blueprint('attendance', __name__)


#GET GENERAL y FILTROS--------------------------------------
@attendance_bp.route("/asistencia", methods=["GET"])
def get_attendance():
    filters = {
        "id_clase": request.args.get("id_clase"),
        "id_alumno": request.args.get("id_alumno"),
    }
    return attendance_service(filters)


#POST-------------------------------------------------------
@attendance_bp.route("/asistencia", methods=["POST"])
def post_attendance():
    data = request.get_json()
    if not data or "id_alumno" not in data or "id_clase" not in data:
        return error_response({
            "code": 400,
            "message": "Bad Request",
            "description": "Los campos 'id_alumno' e 'id_clase' son obligatorios"
        })
    return create_attendance_service(data)


#PATCH ID---------------------------------------------------
@attendance_bp.route("/asistencia/<int:id>", methods=["PATCH"])
def patch_attendance(id):
    if id <= 0:
        return error_response({
            "code": 400,
            "message": "Bad Request",
            "description": "El ID debe ser un número entero positivo"
        })
    data = request.get_json()
    if not data or "presente" not in data:
        return error_response({
            "code": 400,
            "message": "Bad Request",
            "description": "El campo 'presente' es obligatorio"
        })
    if not isinstance(data["presente"], bool):
        return error_response({
            "code": 400,
            "message": "Bad Request",
            "description": "El campo 'presente' debe ser un booleano"
        })
    return patch_attendance_service(id, data)


#DELETE ID--------------------------------------------------
@attendance_bp.route("/asistencia/<int:id>", methods=["DELETE"])
def delete_attendance(id):
    if id <= 0:
        return error_response({
            "code": 400,
            "message": "Bad Request",
            "description": "El ID debe ser un número entero positivo"
        })
    return delete_attendance_service(id)
