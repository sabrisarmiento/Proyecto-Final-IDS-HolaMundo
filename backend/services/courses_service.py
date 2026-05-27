from helpers.responses import error_response, success_response
from controllers.courses_controller import (
    get_all_courses, get_course_id, create_course, 
    patch_course, delete_course
)

def courses_service(filters):
    result = get_all_courses(filters)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "courses": result["data"]
    })

def course_service(id_course):
    result = get_course_id(id_course)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "course": result["data"]
    })

def create_course_service(data):
    result = create_course(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    }, 201)

def patch_course_service(id_course, data):
    result = patch_course(id_course, data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })

def delete_course_service(id_course):
    result = delete_course(id_course)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })