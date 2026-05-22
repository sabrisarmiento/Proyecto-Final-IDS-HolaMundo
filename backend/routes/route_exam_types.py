from flask import Blueprint
from services.exam_types_service import (
    exam_types_get_handler,
    exam_type_get_handler,
    exam_type_post_handler,
    exam_type_patch_handler,
    exam_type_delete_handler,
)

exam_types_bp = Blueprint('exam_types', __name__)

@exam_types_bp.route("/tipos-evaluacion", methods=["GET"])
def get_exam_types():
    return exam_types_get_handler()

@exam_types_bp.route("/tipos-evaluacion/<int:id>", methods=["GET"])
def get_exam_type(id):
    return exam_type_get_handler(id)

@exam_types_bp.route("/tipos-evaluacion", methods=["POST"])
def post_exam_type():
    return exam_type_post_handler()

@exam_types_bp.route("/tipos-evaluacion/<int:id>", methods=["PATCH"])
def patch_exam_type(id):
    return exam_type_patch_handler(id)

@exam_types_bp.route("/tipos-evaluacion/<int:id>", methods=["DELETE"])
def delete_exam_type(id):
    return exam_type_delete_handler(id)
