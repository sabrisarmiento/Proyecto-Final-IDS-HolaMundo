from flask import jsonify
from controller.assistant_controller import get_all_assistants, get_assistant_by_id

def assistants_handler():
  try:
    response = get_all_assistants()

    if not response:
      return jsonify({"assistants": []}), 204

    return jsonify({"assistants": response}), 200

  except Exception as error:
    return jsonify({"errors": [{
      "code": "500",
      "message": "Internal Server Error",
      "level": "error",
      "description": str(error)
    }]}), 500
  
def assistant_handler(id):
  try:
    response = get_assistant_by_id(id)

    if id <= 0:
      return jsonify({ "errors": [{
        "code": "400",
        "message": "Bad Request",
        "level": "error",
        "description": "El ID debe ser un número entero positivo"
      }]}), 400

    return jsonify({"assistant": response}), 200

  except Exception as error:
    return jsonify({"errors": [{
      "code": "500",
      "message": f"Error al obtener el asistente con ID {id}",
      "level": "error",
      "description": str(error)
    }]}), 500