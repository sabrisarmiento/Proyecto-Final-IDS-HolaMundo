from flask import Blueprint
from handlers.exam_handler import (
    exams_handler,
    exam_handler,
    create_exam_handler,
    patch_exam_handler,
    delete_exam_handler
)

exam_bp = Blueprint('exam', __name__)

#GET GENERAL y GET TIPO Y FECHA------------------------------
@exam_bp.route("/evaluaciones", methods=["GET"])
def obtain_exams_params():
    return exams_handler()

#GET ID------------------------------------------------------
@exam_bp.route("/examenes/<int:id>",methods=["GET"])
def obtain_exam_id(id_exam):
    return exam_handler(id_exam)

#POST--------------------------------------------------------
@exam_bp.route("/examenes", methods=["POST"]) 
def add_exam():
    return create_exam_handler()

#PATCH ID----------------------------------------------------
@exam_bp.route("/examenes/<int:id>", methods=["PATCH"])
def modify_exam(id_exam):
    return patch_exam_handler(id_exam)
 

#DELETE ID---------------------------------------------------
@exam_bp.route("/examenes/<int:id>", methods=["DELETE"])
def delete_exam(id_exam):
    return delete_exam_handler(id_exam)
