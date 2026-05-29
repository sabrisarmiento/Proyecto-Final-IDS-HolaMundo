from flask import Blueprint, request
from services.exam_types_service import (
    exam_types_get_handler,
    exam_type_get_handler,
    exam_type_post_handler,
    exam_type_patch_handler,
    exam_type_delete_handler,
)
from middleware.auth_middleware import require_auth

exam_types_bp = Blueprint('exam_types', __name__)

@exam_types_bp.route("/tipos-evaluacion", methods=["GET"])
def get_exam_types():
    return exam_types_get_handler()

@exam_types_bp.route("/tipos-evaluacion/<int:id>", methods=["GET"])
def get_exam_type(id):
    return exam_type_get_handler(id)


@exam_types_bp.route("/tipos-evaluacion", methods=["POST"])
@require_auth
def post_exam_type():
    data = request.get_json()
    return exam_type_post_handler(data)


@exam_types_bp.route("/tipos-evaluacion/<int:id>", methods=["PATCH"])
@require_auth
def patch_exam_type(id):
    data = request.get_json()
    return exam_type_patch_handler(id, data)


@exam_types_bp.route("/tipos-evaluacion/<int:id>", methods=["DELETE"])
@require_auth
def delete_exam_type(id):
    return exam_type_delete_handler(id)
