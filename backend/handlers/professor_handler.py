from flask import jsonify
from controller.professor_controller import get_all_professors

def professors_handler():
  try:
    response = get_all_professors()

    if not response:
      return jsonify({"professors": []}), 200
    
    return jsonify({"professors": response}), 200
  
  except Exception as error:
    return jsonify({"errors": [{
      "code": "500",
      "message": "Internal Server Error",
      "level": "error",
      "description": str(error)
    }]}), 500