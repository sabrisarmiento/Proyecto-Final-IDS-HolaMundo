from flask import jsonify, request
from controller.exam_controller import get_all_exams, create_exam, get_exam_by_id, patch_exam_by_id, delete_exam_by_id

def exams_handler():

    filters = request.args

    result = get_all_exams(filters)

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
        "exams": result["data"]
    }), 200


def create_exam_handler():
    data = request.get_json()
    result = create_exam(data)
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

def exam_handler(id_exam):
    result = get_exam_by_id(id_exam)
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
        "exam": result["data"]
    }), 200


def patch_exam_handler(id_exam):
    data = request.get_json()
    result = patch_exam_by_id(id_exam, data)
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

def delete_exam_handler(id_exam):
    result = delete_exam_by_id(id_exam)
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