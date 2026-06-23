from helpers.responses import error_response, success_response
from helpers.user_belongs import user_can_manage_evaluacion, user_can_manage_nota
from controllers.marks_controller import get_all_marks, create_mark, get_mark_by_id, patch_mark_by_id, delete_mark_by_id

def marks_service(filters):
    result = get_all_marks(filters)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "marks": result["data"]
    })

def create_mark_service(data, user):
    if not user_can_manage_evaluacion((data or {}).get("id_evaluacion"), user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre esta evaluación"
        })
    result = create_mark(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    }, 201)

def mark_service(id_mark):
    result = get_mark_by_id(id_mark)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "mark": result["data"]
    })


def patch_mark_service(id_mark, data, user):
    if not user_can_manage_nota(id_mark, user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre esta nota"
        })
    result = patch_mark_by_id(id_mark, data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })

def delete_mark_service(id_mark, user):
    if not user_can_manage_nota(id_mark, user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre esta nota"
        })
    result = delete_mark_by_id(id_mark)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })
