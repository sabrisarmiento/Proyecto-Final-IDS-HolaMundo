from helpers.responses import error_response, success_response
from controllers.attendance_controller import (
    get_all_attendance,
    create_attendance,
    update_attendance,
    delete_attendance,
)


def attendance_service(filters):
    result = get_all_attendance(filters)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "attendance": result["data"]
    })


def create_attendance_service(data):
    result = create_attendance(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "id_asistencia": result["data"]
    }, 201)


def patch_attendance_service(id, data):
    result = update_attendance(id, data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })


def delete_attendance_service(id):
    result = delete_attendance(id)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })
