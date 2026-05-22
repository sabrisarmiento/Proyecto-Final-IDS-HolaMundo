from flask import jsonify, request
from controllers.materials_controller import get_all_materials, create_material, delete_material_by_id



def materials_handler():
    filters = request.args
    result = get_all_materials(filters)
    if not result["ok"]:
        return jsonify({
            "errors": [{
                "code": result["code"],
                "message": result["message"],
                "level": "error",
                "description": result["description"]
            }]
        }), result["code"]

    return jsonify({
        "materials": result["data"]
    }), 200

def create_material_handler():
    data = request.get_json()
    result = create_material(data)
    if not result["ok"]:
        return jsonify({
            "errors": [{
                "code": result["code"],
                "message": result["message"],
                "level": "error",
                "description": result["description"]
            }]
        }), result["code"]
    return jsonify({
        "message": result["message"]
    }), 201

def delete_material_handler(id_material):
    result = delete_material_by_id(id_material)
    if not result["ok"]:
        return jsonify({
            "errors": [{
                "code": result["code"],
                "message": result["message"],
                "level": "error",
                "description": result["description"]
            }]
        }), result["code"]
    return jsonify({
        "message": result["message"]
    }), 200