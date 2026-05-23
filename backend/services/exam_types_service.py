from helpers.responses import error_response, success_response
from controllers.exam_types_controller import (
    get_all_exam_types,
    get_exam_type_by_id,
    create_exam_type,
    update_exam_type,
    delete_exam_type,
)


def exam_types_service():
    result = get_all_exam_types()
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "exam_types": result["data"]
    })


def exam_type_service(id):
    result = get_exam_type_by_id(id)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "exam_type": result["data"]
    })


def create_exam_type_service(data):
    result = create_exam_type(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "id_tipo": result["data"]
    }, 201)


def patch_exam_type_service(id, data):
    result = update_exam_type(id, data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })


def delete_exam_type_service(id):
    result = delete_exam_type(id)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })
