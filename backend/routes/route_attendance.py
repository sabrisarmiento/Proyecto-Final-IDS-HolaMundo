from flask import Blueprint
from services.attendance_service import (
    attendance_get_handler,
    attendance_post_handler,
    attendance_patch_handler,
    attendance_delete_handler,
)
from middleware.auth_middleware import require_auth

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route("/asistencia", methods=["GET"])
def get_attendance():
    return attendance_get_handler()

@attendance_bp.route("/asistencia", methods=["POST"])
def post_attendance():
    return attendance_post_handler()


@attendance_bp.route("/asistencia/<int:id>", methods=["PATCH"])
@require_auth
def patch_attendance(id):
    return attendance_patch_handler(id)


@attendance_bp.route("/asistencia/<int:id>", methods=["DELETE"])
@require_auth
def delete_attendance(id):
    return attendance_delete_handler(id)
