from helpers.responses import error_response, success_response
from controllers.dashboard_course_controller import get_course_dashboard


def course_dashboard_service(id_curso):
    result = get_course_dashboard(id_curso)
    if not result["ok"]:
        return error_response(result)
    return success_response({"dashboard": result["data"]})