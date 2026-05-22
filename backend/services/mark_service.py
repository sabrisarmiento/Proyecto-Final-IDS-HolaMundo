from helpers.responses import error_response, success_response
from controllers.marks_controller import get_all_marks, create_mark, get_mark_by_id, patch_mark_by_id, delete_mark_by_id

def marks_handler(filters):
    result = get_all_marks(filters)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "marks": result["data"]
    })

def create_mark_handler(data):
    result = create_mark(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    }, 201)

def mark_handler(id_mark):
    result = get_mark_by_id(id_mark)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "mark": result["data"]
    })


def patch_mark_handler(id_mark, data):
    result = patch_mark_by_id(id_mark, data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })

def delete_mark_handler(id_mark):
    result = delete_mark_by_id(id_mark)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })
