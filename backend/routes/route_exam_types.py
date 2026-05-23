from flask import Blueprint, request
from services.exam_types_service import (
    exam_types_service,
    exam_type_service,
    create_exam_type_service,
    patch_exam_type_service,
    delete_exam_type_service,
)
from helpers.responses import error_response

exam_types_bp = Blueprint('exam_types', __name__)

CAMPOS_VALIDOS = {"nombre", "descripcion"}


#GET GENERAL------------------------------------------------
@exam_types_bp.route("/tipos-evaluacion", methods=["GET"])
def get_exam_types():
    return exam_types_service()


#GET ID-----------------------------------------------------
@exam_types_bp.route("/tipos-evaluacion/<int:id>", methods=["GET"])
def get_exam_type(id):
    if id <= 0:
        return error_response({
            "code": 400,
            "message": "Bad Request",
            "description": "El ID debe ser un número entero positivo"
        })
    return exam_type_service(id)


#POST-------------------------------------------------------
@exam_types_bp.route("/tipos-evaluacion", methods=["POST"])
def post_exam_type():
    data = request.get_json()
    if not data or "nombre" not in data:
        return error_response({
            "code": 400,
            "message": "Bad Request",
            "description": "El campo 'nombre' es obligatorio"
        })
    return create_exam_type_service(data)


#PATCH ID---------------------------------------------------
@exam_types_bp.route("/tipos-evaluacion/<int:id>", methods=["PATCH"])
def patch_exam_type(id):
    if id <= 0:
        return error_response({
            "code": 400,
            "message": "Bad Request",
            "description": "El ID debe ser un número entero positivo"
        })
    data = request.get_json()
    if not data:
        return error_response({
            "code": 400,
            "message": "Bad Request",
            "description": "Debe enviar al menos un campo para actualizar"
        })
    for campo in data:
        if campo not in CAMPOS_VALIDOS:
            return error_response({
                "code": 400,
                "message": "Bad Request",
                "description": f"El campo '{campo}' no es válido"
            })
    return patch_exam_type_service(id, data)


#DELETE ID--------------------------------------------------
@exam_types_bp.route("/tipos-evaluacion/<int:id>", methods=["DELETE"])
def delete_exam_type(id):
    if id <= 0:
        return error_response({
            "code": 400,
            "message": "Bad Request",
            "description": "El ID debe ser un número entero positivo"
        })
    return delete_exam_type_service(id)
