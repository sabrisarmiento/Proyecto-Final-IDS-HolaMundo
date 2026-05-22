from flask import jsonify, request
from controllers.attendance_controller import (
    get_attendance,
    create_attendance,
    update_attendance,
    delete_attendance,
)

def attendance_get_handler():
    try:
        id_clase = request.args.get("id_clase")
        id_alumno = request.args.get("id_alumno")
        result = get_attendance(id_clase, id_alumno)
        if not result:
            return jsonify({"attendance": []}), 204
        return jsonify({"attendance": result}), 200
    except Exception as error:
        return jsonify({"errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(error)
        }]}), 500

def attendance_post_handler():
    try:
        data = request.get_json()
        if not data or "id_alumno" not in data or "id_clase" not in data:
            return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Los campos 'id_alumno' e 'id_clase' son obligatorios"
            }]}), 400
        new_id = create_attendance(data)
        return jsonify({"id_asistencia": new_id}), 201
    except Exception as error:
        return jsonify({"errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(error)
        }]}), 500

def attendance_patch_handler(id):
    try:
        if id <= 0:
            return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El ID debe ser un número entero positivo"
            }]}), 400
        data = request.get_json()
        if not data or "presente" not in data:
            return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El campo 'presente' es obligatorio"
            }]}), 400
        if not isinstance(data["presente"], bool):
            return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El campo 'presente' debe ser un booleano"
            }]}), 400
        if not update_attendance(id, data["presente"]):
            return jsonify({"errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": f"No existe un registro de asistencia con ID {id}"
            }]}), 404
        return "", 204
    except Exception as error:
        return jsonify({"errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(error)
        }]}), 500

def attendance_delete_handler(id):
    try:
        if id <= 0:
            return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El ID debe ser un número entero positivo"
            }]}), 400
        if not delete_attendance(id):
            return jsonify({"errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": f"No existe un registro de asistencia con ID {id}"
            }]}), 404
        return "", 204
    except Exception as error:
        return jsonify({"errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(error)
        }]}), 500
