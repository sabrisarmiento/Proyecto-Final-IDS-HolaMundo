from helpers.responses import error_response, success_response
from controllers.subject_controller import (
    get_all_subjects,
    get_subject_by_id,
    create_subject,
    patch_subject,
    delete_subject,
    get_subjects_for_user
)

def subjects_service(filters):
  result = get_all_subjects(filters)
  if not result["ok"]:
    return error_response(result)
  return success_response({
    "subjects": result["data"]
  })

def subject_service(subject_id):
  result = get_subject_by_id(subject_id)
  if not result["ok"]:
    return error_response(result)
  return success_response({
    "subject": result["data"]
  })

def my_subjects_service(id_user, is_admin, filters):
    result = get_subjects_for_user(id_user, is_admin, filters)
    if not result["ok"]:
        return error_response(result)
    return success_response({"subjects": result["data"]})


def create_subject_service(data):
  result = create_subject(data)
  if not result["ok"]:
    return error_response(result)
  return success_response({
    "message": result["message"]
  }, 201)

def patch_subject_service(subject_id, data):
  result = patch_subject(subject_id, data)
  if not result["ok"]:
    return error_response(result)
  return success_response({
    "message": result["message"]
  })

def delete_subject_service(subject_id):
  result = delete_subject(subject_id)
  if not result["ok"]:
    return error_response(result)
  return success_response({
    "message": result["message"]
  })