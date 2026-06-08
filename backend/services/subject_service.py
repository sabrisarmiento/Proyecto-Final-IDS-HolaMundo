from helpers.responses import error_response, success_response
from controllers.subject_controller import (
    get_all_subjects,
    get_subject_by_id,
    create_subject
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

def create_subject_service(data):
  result = create_subject(data)
  if not result["ok"]:
    return error_response(result)
  return success_response({
    "message": result["message"]
  }, 201)