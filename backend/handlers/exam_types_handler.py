from flask import jsonify, request
from controller.exam_types_controller import (
    get_all_exam_types,
    get_exam_type_by_id,
    create_exam_type,
    update_exam_type,
    delete_exam_type,
)

def exam_types_get_handler():
    try:
        result = get_all_exam_types()
        if not result:
            return jsonify({"exam_types": []}), 204
        return jsonify({"exam_types": result}), 200
    except Exception as error:
        return jsonify({"errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(error)
        }]}), 500

def exam_type_get_handler(id):
    try:
        if id <= 0:
            return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El ID debe ser un número entero positivo"
            }]}), 400
        result = get_exam_type_by_id(id)
        if not result:
            return jsonify({"errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": f"No existe un tipo de evaluación con ID {id}"
            }]}), 404
        return jsonify({"exam_type": result}), 200
    except Exception as error:
        return jsonify({"errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(error)
        }]}), 500

def exam_type_post_handler():
    try:
        data = request.get_json()
        if not data or "nombre" not in data:
            return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El campo 'nombre' es obligatorio"
            }]}), 400
        new_id = create_exam_type(data)
        return jsonify({"id_tipo": new_id}), 201
    except Exception as error:
        return jsonify({"errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(error)
        }]}), 500

def exam_type_patch_handler(id):
    try:
        if id <= 0:
            return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El ID debe ser un número entero positivo"
            }]}), 400
        data = request.get_json()
        if not data:
            return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Debe enviar al menos un campo para actualizar"
            }]}), 400
        campos_validos = {"nombre", "descripcion"}
        for campo in data:
            if campo not in campos_validos:
                return jsonify({"errors": [{
                    "code": "400",
                    "message": "Bad Request",
                    "level": "error",
                    "description": f"El campo '{campo}' no es válido"
                }]}), 400
        if not get_exam_type_by_id(id):
            return jsonify({"errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": f"No existe un tipo de evaluación con ID {id}"
            }]}), 404
        update_exam_type(id, data)
        return "", 204
    except Exception as error:
        return jsonify({"errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(error)
        }]}), 500

def exam_type_delete_handler(id):
    try:
        if id <= 0:
            return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El ID debe ser un número entero positivo"
            }]}), 400
        if not delete_exam_type(id):
            return jsonify({"errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": f"No existe un tipo de evaluación con ID {id}"
            }]}), 404
        return "", 204
    except Exception as error:
        return jsonify({"errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(error)
        }]}), 500
