from flask import jsonify, request
from controller.marks_controller import get_all_marks, create_mark, get_mark_by_id, patch_mark_by_id, delete_mark_by_id

def marks_handler():

    filters = request.args

    result = get_all_marks(filters)

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
        "marks": result["data"]
    }), 200


def create_mark_handler():
    data = request.get_json()
    result = create_mark(data)
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

def mark_handler(id_mark):
    result = get_mark_by_id(id_mark)
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
        "mark": result["data"]
    }), 200


def patch_mark_handler(id_mark):
    data = request.get_json()
    result = patch_mark_by_id(id_mark, data)
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

def delete_mark_handler(id_mark):
    result = delete_mark_by_id(id_mark)
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
