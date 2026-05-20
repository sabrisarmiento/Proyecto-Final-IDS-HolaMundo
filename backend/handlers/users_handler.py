from flask import jsonify, request
from controller.users_controller import get_all_users, create_user, get_user_by_id, update_user_by_id, delete_user_by_id

def users_handler():
  filters = request.args
  response = get_all_users(filters)

  if not response["ok"]:
    return jsonify({
      "errors": [{
        "code": response["code"],
        "message": response["message"],
        "level": "error",
        "description": response["description"]
      }]
    }), response["code"]
  
  return jsonify({
    "users": response["data"]
  }), 200

def user_handler(id_usuario):
  response = get_user_by_id(id_usuario)

  if not response["ok"]:
    return jsonify({
      "errors": [{
        "code": response["code"],
        "message": response["message"],
        "level": "error",
        "description": response["description"]
      }]
    }), response["code"]
  
  return jsonify({
    "user": response["data"]
  }), 200

def create_user_handler():
  data = request.get_json()
  response = create_user(data)

  if not response["ok"]:
    return jsonify({
      "errors": [{
        "code": response["code"],
        "message": response["message"],
        "level": "error",
        "description": response["description"]
      }]
    }), response["code"]
  
  return jsonify({
    "message": response["message"]
  }), 201

def patch_user_handler(id_usuario):
  data = request.get_json()
  response = update_user_by_id(id_usuario, data)

  if not response["ok"]:
    return jsonify({
      "errors": [{
        "code": response["code"],
        "message": response["message"],
        "level": "error",
        "description": response["description"]
      }]
    }), response["code"]
  
  return jsonify({
    "message": response["message"]
  }), 200

def delete_user_handler(id_usuario):
  response = delete_user_by_id(id_usuario)

  if not response["ok"]:
    return jsonify({
      "errors": [{
        "code": response["code"],
        "message": response["message"],
        "level": "error",
        "description": response["description"]
      }]
    }), response["code"]
  
  return jsonify({
    "message": response["message"]
  }), 200