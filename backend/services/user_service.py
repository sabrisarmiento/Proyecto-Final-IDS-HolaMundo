from helpers.responses import error_response, success_response
from controllers.users_controller import get_all_users, create_user, get_user_by_id, update_user_by_id, delete_user_by_id

def users_service(filters):
  result = get_all_users(filters)
  if not result["ok"]:
      return error_response(result)
  return success_response({
    "users": result["data"]
  })

def user_service(id_user):
  result = get_user_by_id(id_user)
  if not result["ok"]:
      return error_response(result)
  return success_response({
    "user": result["data"]
  })

def create_user_service(data, logged_user):
  result = create_user(data, logged_user)
  if not result["ok"]:
      return error_response(result)
  return success_response({
    "message": result["message"]
  }, 201)


def patch_user_service(id_user, data, logged_user):
  result = update_user_by_id(id_user, data, logged_user)
  if not result["ok"]:
      return error_response(result)
  return success_response({
    "message" : result["message"]
  })

def delete_user_service(id_user, logged_user):
  result = delete_user_by_id(id_user, logged_user)
  if not result["ok"]:
      return error_response(result)
  return success_response({
    "message": result["message"]
  })