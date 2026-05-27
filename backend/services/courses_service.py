from helpers.responses import error_response, success_response
from controllers.courses_controller import get_all_courses

def courses_service():
  result = get_all_courses()
  if not result["ok"]:
    return error_response(result)
  return success_response({
    "courses": result["data"]
  })