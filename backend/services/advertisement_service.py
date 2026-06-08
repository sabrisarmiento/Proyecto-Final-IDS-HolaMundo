from helpers.responses import error_response, success_response
from controllers.advertisement_controller import get_all_advertisements, create_advertisement, get_advertisement_by_id, patch_advertisement_by_id, delete_advertisement_by_id, get_advertisements_by_subject

def advertisements_service(filters):
  result = get_all_advertisements(filters)
  if not result["ok"]:
      return error_response(result)
  return success_response({
      "advertisements": result["data"]
  })

def create_advertisement_service(data, user):
  result = create_advertisement(data, user)
  if not result["ok"]:
      return error_response(result)
  return success_response({
      "message": result["data"]
  }, 201)

def advertisement_service(id_advertisement):
  result = get_advertisement_by_id(id_advertisement)
  if not result["ok"]:
      return error_response(result)
  return success_response({
      "advertisement": result["data"]
  })

def patch_advertisement_service(id_advertisement, data):
  result = patch_advertisement_by_id(id_advertisement, data)
  if not result["ok"]:
      return error_response(result)
  return success_response({
      "message": result["message"]
  })

def delete_advertisement_service(id_advertisement):
  result = delete_advertisement_by_id(id_advertisement)
  if not result["ok"]:
      return error_response(result)
  return success_response({
      "message": result["message"]
  })

def advertisements_by_subject_service(id_materia):
    result = get_advertisements_by_subject(id_materia)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "advertisements": result["data"]
    })