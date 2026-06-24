from helpers.responses import error_response, success_response
from helpers.user_belongs import user_can_manage_course, user_can_manage_evaluacion
from controllers.exam_controller import (
    get_all_exams,
    create_exam,
    get_exam_by_id,
    patch_exam_by_id,
    delete_exam_by_id,
    save_notes_to_db,
    get_students_with_notes_db,
    get_promocion_config_db,
    save_promocion_config_db,
)

def exams_service(filters):
    result = get_all_exams(filters)
    if not result["ok"]:
        return error_response(result)
    return success_response({"evaluaciones": result['data']})

def create_exam_service(data, user):
    if not user_can_manage_course((data or {}).get("id_curso"), user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre este curso"
        })
    result = create_exam(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({"message": result["message"]}, 201)

def exam_service(id_exam):
    result = get_exam_by_id(id_exam)
    if not result["ok"]:
        return error_response(result)
    return success_response({"exams": result['data']})

def patch_exam_service(id_exam, data, user):
    if not user_can_manage_evaluacion(id_exam, user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre esta evaluación"
        })
    result = patch_exam_by_id(id_exam, data)
    if not result["ok"]:
        return error_response(result)
    return success_response({"message": result["message"]})

def delete_exam_service(id_exam, user):
    if not user_can_manage_evaluacion(id_exam, user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre esta evaluación"
        })
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

def students_notes_report_service(id_curso, page=1, per_page=None, order_by=None, order='asc'):
    if not id_curso:
        return error_response({
            "ok": False, "code": 400,
            "message": "Bad Request", "description": "ID de curso requerido"
        })

    limit = int(per_page) if per_page else None
    offset = (int(page) - 1) * limit if limit else 0

    result = get_students_with_notes_db(id_curso, limit=limit, offset=offset, order_by=order_by, order=order)

    if not result["ok"]:
        return error_response(result)
    return success_response({"data": result['data'], "total": result['total']})
# def students_notes_report_service(id_curso):
#     if not id_curso:
#         return error_response({
#             "ok": False, "code": 400,
#             "message": "Bad Request", "description": "ID de curso requerido"
#         })

#     result = get_students_with_notes_db(id_curso)

#     if not result["ok"]:
#         return error_response(result)
#     return success_response({"data": result['data']})

# PROMOCION

def get_promocion_config_service(id_curso):
    if not id_curso:
        return error_response({
            "ok": False, "code": 400,
            "message": "Bad Request", "description": "id_curso requerido"
        })
    result = get_promocion_config_db(id_curso)
    if not result["ok"]:
        return error_response(result)
    return success_response({"config": result["data"]})


def save_promocion_config_service(id_curso, data, user):
    if not user_can_manage_course(id_curso, user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre este curso"
        })
    if not id_curso or not data:
        return error_response({
            "ok": False, "code": 400,
            "message": "Bad Request", "description": "Datos requeridos"
        })
    es_promocionable      = data.get("es_promocionable", False)
    evaluaciones          = data.get("evaluaciones", [])
    cuenta_asistencia     = data.get("cuenta_asistencia", False)
    porcentaje_asistencia = float(data.get("porcentaje_asistencia", 75.0))

    result = save_promocion_config_db(
        id_curso, es_promocionable, evaluaciones,
        cuenta_asistencia, porcentaje_asistencia
    )
    if not result["ok"]:
        return error_response(result)
    return success_response({"message": result["message"]})