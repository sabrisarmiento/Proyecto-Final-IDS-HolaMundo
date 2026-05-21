from flask import jsonify

def error_response(result):
    return jsonify({
        "errors": [{
                "code": result["code"],
                "message": result["message"],
                "level": "error",
                "description": result["description"]
            }]
    }), result["code"]

def success_response(response, status_code=200):
    return jsonify(response), status_code