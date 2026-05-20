from flask import jsonify, request
from controller.classes_controller import get_classes, get_class_id, create_class, update_class

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