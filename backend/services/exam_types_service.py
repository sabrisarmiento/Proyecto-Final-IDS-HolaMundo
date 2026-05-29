from helpers.responses import error_response, success_response
from controllers.exam_types_controller import (
    get_all_exam_types,
    get_exam_type_by_id,
    create_exam_type,
    update_exam_type,
    delete_exam_type,
)

def exam_types_get_handler():
    result = get_all_exam_types()
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "exam_types": result["data"]
    })

def exam_type_get_handler(id):
    result = get_exam_type_by_id(id)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "exam_type": result["data"]
    })

def exam_type_post_handler(data):
    result = create_exam_type(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    }, 201)

def exam_type_patch_handler(id, data):
    result = update_exam_type(id, data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })

def exam_type_delete_handler(id):
    result = delete_exam_type(id)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })
