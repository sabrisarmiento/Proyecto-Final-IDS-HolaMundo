from helpers.responses import error_response, success_response
from controllers.subject_controller import (
    get_all_subjects,
    get_subject_by_id,
    get_topics_by_subject_id,
    create_subject,
    patch_subject,
    delete_subject,
    get_subjects_for_user,
    get_professors_by_subject,
    assign_professor_to_subject,
    remove_professor_from_subject
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


def get_topics_service(subject_id):
    result = get_topics_by_subject_id(subject_id)
    if not result["ok"]:
        return error_response(result)
    return success_response({"topics": result["data"]})

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

def get_professors_by_subject_service(id_materia):
    result = get_professors_by_subject(id_materia)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "professors": result["data"]
    })

def assign_professor_to_subject_service(id_materia, data):
    id_profesor = data.get("id_profesor")
    result = assign_professor_to_subject(id_materia, id_profesor)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })

def remove_professor_from_subject_service(id_materia, id_profesor):
    result = remove_professor_from_subject(id_materia, id_profesor)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })