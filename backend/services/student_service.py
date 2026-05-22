from helpers.responses import error_response, success_response
from controllers.students_controller import (
    get_all_students,
    get_student_by_id,
    create_student,
    import_students_from_csv,
)

def fetch_students_service(filters):
    result = get_all_students(filters)
    if not result["ok"]:
        return error_response(result)
    if not result["data"]:
        return "", 204
    return success_response({"students": result["data"]})


def fetch_student_id_service(id):
    result = get_student_by_id(id)
    if not result["ok"]:
        return error_response(result)
    return success_response({"student": result["data"]})


def create_student_service(data):
    result = create_student(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"],
        "id": result["id"],
    }, 201)


def import_students_service(files):
    result = import_students_from_csv(files)
    if not result["ok"]:
        return error_response(result)
    return success_response(result["data"], result.get("status", 201))