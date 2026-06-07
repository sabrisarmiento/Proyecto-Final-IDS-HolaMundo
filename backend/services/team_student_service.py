from helpers.responses import error_response, success_response
from controllers.team_student_controller import add_student_to_team

def add_student_to_team_service(data):
    result = add_student_to_team(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })