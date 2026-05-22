from flask import jsonify, request
from controllers.classes_controller import get_classes, get_class_id, create_class, update_class, delete_class

def classes_handler():
    filters = request.args
    result = get_classes(filters)
    if not result["ok"]:
        return jsonify({"errors": [{
            "code": result["code"],
            "message": result["message"],
            "level": "error",
            "description": result["description"]
            }]}), result["code"]

    return jsonify({
        "classes": result["data"]
    }), 200

def class_get_handler(id_clase):
    result = get_class_id(id_clase)
    if not result["ok"]:
        return jsonify({"errors": [{
            "code": result["code"],
            "message": result["message"],
            "level": "error",
            "description": result["description"]
            }]}), result["code"]
    
    return jsonify({
        "classes": result["data"]
    }), 200            

def class_post_handler():
    data = request.get_json()
    result = create_class(data)
    if not result["ok"]:
        return jsonify({"errors": [{
            "code": result["code"],
            "message": result["message"],
            "level": "error",
            "description": result["description"]
            }]}), result["code"]
    
    return jsonify({
        "classes": result["data"]
    }), 201

def class_patch_handler(id_clase):
    data = request.get_json()
    result = update_class(id_clase, data)
    if not result["ok"]:
        return jsonify({"errors": [{
            "code": result["code"],
            "message": result["message"],
            "level": "error",
            "description": result["description"]
            }]}), result["code"]
    
    return jsonify({
        "classes": result["data"]
    }), 200

def delete_class_handler(id):
    try:
        if id <= 0:
            return jsonify({
                "errors": [{
                    "code": 400,
                    "message": "ID inválido"
                }]
            }), 400
        delete_class(id)
        return jsonify({
            "message": "Clase eliminada correctamente"
        }), 200
    except Exception as error:
        return jsonify({
            "errors": [{
                "code": 500,
                "message": "Error al eliminar clase",
                "description": str(error)
            }]
        }), 500