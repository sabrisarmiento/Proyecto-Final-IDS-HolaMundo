from flask import Blueprint, request
from services.attendance_service import (
    attendance_get_handler,
    attendance_post_handler,
    attendance_patch_handler,
    attendance_delete_handler,
    generate_qr_service, 
)
from middleware.auth_middleware import require_auth

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route("/asistencia", methods=["GET"])
def get_attendance():
    id_clase = request.args.get("id_clase")
    id_alumno = request.args.get("id_alumno")
    return attendance_get_handler(id_clase, id_alumno)

@attendance_bp.route("/asistencia", methods=["POST"])
def post_attendance():
    data = request.get_json()
    return attendance_post_handler(data)

@attendance_bp.route("/asistencia/generar-qr", methods=["POST"])
def post_generate_qr():
    data = request.get_json()
    return generate_qr_service(data.get("id_clase"))

@attendance_bp.route("/asistencia/<int:id>", methods=["PATCH"])
@require_auth
def patch_attendance(id):
    data = request.get_json()
    return attendance_patch_handler(id, data)


@attendance_bp.route("/asistencia/<int:id>", methods=["DELETE"])
@require_auth
def delete_attendance(id):
    return attendance_delete_handler(id)