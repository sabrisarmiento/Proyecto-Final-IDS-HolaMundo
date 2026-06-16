from helpers.responses import error_response, success_response
from controllers.courses_controller import (
    get_all_courses, get_course_id, create_course, 
    patch_course, delete_course, get_courses_for_user, assign_assistant_to_course, 
    get_assistants_by_course, remove_assistant_from_course
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

def my_courses_service(id_user, is_admin, filters):
    result = get_courses_for_user(id_user, is_admin, filters)
    if not result["ok"]:
        return error_response(result)
    return success_response({"courses": result["data"]})

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

def assign_assistant_to_course_service(id_curso, data, user):
    result = assign_assistant_to_course(
        id_curso,
        data.get("id_ayudante"),
        user["id_usuario"],
        user["id_rol"]
    )
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })

def get_assistants_by_course_service(id_curso):
    result = get_assistants_by_course(id_curso)

    if not result["ok"]:
        return error_response(result)

    return success_response({
        "assistants": result["data"]
    })

def remove_assistant_from_course_service(id_curso, id_ayudante):
    result = remove_assistant_from_course(id_curso, id_ayudante)

    if not result["ok"]:
        return error_response(result)

    return success_response({
        "message": result["message"]
    })