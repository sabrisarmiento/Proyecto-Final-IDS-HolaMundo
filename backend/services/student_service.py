from helpers.responses import error_response, success_response
from helpers.user_belongs import user_can_manage_course, user_can_manage_alumno
from controllers.students_controller import (
    get_all_students,
    get_student_by_id,
    create_student,
    import_students_from_csv,
    update_student
)

def students_service(filters):
    result = get_all_students(filters)
    if not result["ok"]:
        return error_response(result)
    if not result["data"]:
        return success_response("", 204)
    return success_response({
        "students": result["data"],
        "total": result["total"],
    })


def student_service(id):
    result = get_student_by_id(id)
    if not result["ok"]:
        return error_response(result)
    return success_response({"student": result["data"]})


def create_student_service(data, user):
    if not user_can_manage_course((data or {}).get("id_curso"), user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre este curso"
        })
    result = create_student(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"],
        "id": result["id"],
    }, 201)


def import_students_service(files, id_curso, user):
    if not user_can_manage_course(id_curso, user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre este curso"
        })
    result = import_students_from_csv(files, id_curso)
    if not result["ok"]:
        return error_response(result)
    return success_response(result["data"], result.get("status", 201))

def update_student_service(student_id, data, user):
    if not user_can_manage_alumno(student_id, user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre este alumno"
        })
    result = update_student(student_id, data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"],
        "id": result["id"],
    }, 200)