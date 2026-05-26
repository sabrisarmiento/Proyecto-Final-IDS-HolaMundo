from flask import Blueprint, request
from services.attendance_service import (
    attendance_get_handler,
    attendance_post_handler,
    attendance_patch_handler,
    attendance_delete_handler,
    generate_qr_service, 
)

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route("/asistencia", methods=["GET"])
def get_attendance():
    return attendance_get_handler()

@attendance_bp.route("/asistencia", methods=["POST"])
def post_attendance():
    return attendance_post_handler()

@attendance_bp.route("/asistencia/generar-qr", methods=["POST"])
def post_generate_qr():
    data = request.get_json()
    return generate_qr_service(data.get("id_clase"))

@attendance_bp.route("/asistencia/<int:id>", methods=["PATCH"])
def patch_attendance(id):
    return attendance_patch_handler(id)

@attendance_bp.route("/asistencia/<int:id>", methods=["DELETE"])
def delete_attendance(id):
    return attendance_delete_handler(id)