from flask import jsonify
from controller.assistant_controller import get_all_assistants, get_assistant_by_id

def assistants_handler():
  response = get_all_assistants()

  if not response["ok"]:
    return jsonify({"errors": [{
      "code": response["code"],
      "message": response["message"],
      "level": "error",
      "description": response["description"]
    }]}), response["code"]

  return jsonify({"assistants": response["data"] or []}), 200

  
def assistant_handler(id):
  response = get_assistant_by_id(id)

  if not response["ok"]:
    return jsonify({"errors": [{
      "code": response["code"],
      "message": response["message"],
      "level": "error",
      "description": response["description"]
    }]}), response["code"]

  if not response["data"]:
    return jsonify({"errors": [{
      "code": 200,
      "message": f"Assistant with ID {id} not found",
      "level": "error",
      "description": f"No assistant found with ID {id}"
    }]}), 200

  return jsonify({"assistant": response["data"]}), 200