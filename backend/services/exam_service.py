from helpers.responses import error_response, success_response
from controllers.exam_controller import (
    get_all_exams,
    create_exam,
    get_exam_by_id,
    patch_exam_by_id,
    delete_exam_by_id,
    save_notes_to_db,
    get_students_with_notes_db
)
 
 
def exams_service(filters):
    result = get_all_exams(filters)
    if not result["ok"]:
        return error_response(result)
    return success_response({"evaluaciones": result['data']})
 
 
def create_exam_service(data):
    result = create_exam(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({"message": result["message"]}, 201)
 
 
def exam_service(id_exam):
    result = get_exam_by_id(id_exam)
    if not result["ok"]:
        return error_response(result)
    return success_response({"exams": result['data']})
 
 
def patch_exam_service(id_exam, data):
    result = patch_exam_by_id(id_exam, data)
    if not result["ok"]:
        return error_response(result)
    return success_response({"message": result["message"]})
 
 
def delete_exam_service(id_exam):
    result = delete_exam_by_id(id_exam)
    if not result["ok"]:
        return error_response(result)
    return success_response({"message": result["message"]})
 
 
def save_exam_notes_service(id_exam, notes_dict, id_corrector, correctores_dict=None):
    """
    id_exam:         int o str con el id de la evaluación
    notes_dict:      {id_alumno: nota}
    id_corrector:    id del usuario logueado (puede ser None)
    correctores_dict: {id_alumno: nombre_corrector} — override por alumno
    """
    if not id_exam or not notes_dict:
        return error_response({
            "ok": False, "code": 400,
            "message": "Bad Request", "description": "Faltan datos"
        })
 
    if correctores_dict is None:
        correctores_dict = {}
 
    result = save_notes_to_db(id_exam, notes_dict, id_corrector, correctores_dict)
 
    if not result["ok"]:
        return error_response(result)
    return success_response({"message": "Notas guardadas con éxito"})
 
 
def students_notes_report_service(id_curso):
    if not id_curso:
        return error_response({
            "ok": False, "code": 400,
            "message": "Bad Request", "description": "ID de curso requerido"
        })
 
    result = get_students_with_notes_db(id_curso)
 
    if not result["ok"]:
        return error_response(result)
    return success_response({"data": result['data']})