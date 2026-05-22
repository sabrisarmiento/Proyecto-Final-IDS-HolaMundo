from flask import Blueprint,request
from services.exam_service import (
    exams_service,
    exam_service,
    create_exam_service,
    patch_exam_service,
    delete_exam_service
)

exam_bp = Blueprint('exam', __name__)

#GET GENERAL y GET TIPO Y FECHA------------------------------
@exam_bp.route("/evaluaciones", methods=["GET"])
def obtain_exams_params():
    filters = {
        "id_tipo": request.args.get('id_tipo'),
        "id_usuario": request.args.get('id_usuario'),
        "fecha": request.args.get('fecha'),
    }
    return exam_service(filters)

#GET ID------------------------------------------------------
@exam_bp.route("/examenes/<int:id>",methods=["GET"])
def obtain_exam_id(id_exam):
    return exam_service(id_exam)

#POST--------------------------------------------------------
@exam_bp.route("/examenes", methods=["POST"]) 
def add_exam():
    return create_exam_service()

#PATCH ID----------------------------------------------------
@exam_bp.route("/examenes/<int:id>", methods=["PATCH"])
def modify_exam(id_exam):
    return patch_exam_service(id_exam)
 

#DELETE ID---------------------------------------------------
@exam_bp.route("/examenes/<int:id>", methods=["DELETE"])
def delete_exam(id_exam):
    return delete_exam_service(id_exam)
