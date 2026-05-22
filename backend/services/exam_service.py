from helpers.responses import error_response, success_response
from controllers.exam_controller import get_all_exams, create_exam, get_exam_by_id, patch_exam_by_id, delete_exam_by_id

def exam_service(filters):
    result = get_all_exams(filters)

    if not result["ok"]:
        return error_response(result)
    return success_response({
        "exams": result['data']
    })


def create_exam_service(data):
    result = create_exam(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    }, 201)

def exam_service(id_exam):
    result = get_exam_by_id(id_exam)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "exams": result['data']
    })


def patch_exam_service(id_exam,data):
    result = patch_exam_by_id(id_exam, data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })

def delete_exam_service(id_exam):
    result = delete_exam_by_id(id_exam)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })
