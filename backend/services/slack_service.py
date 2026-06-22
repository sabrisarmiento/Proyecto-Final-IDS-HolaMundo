from controllers.slack_controller import configure_slack_course, get_slack_messages, disconnect_slack_course
from helpers.responses import error_response, success_response

def configure_slack_course_service(id_curso, data, user):
    id_usuario = user["id_usuario"]

    result = configure_slack_course(id_curso, data, id_usuario)

    if not result["ok"]:
        return error_response(result)

    return success_response({
        "message": result["data"]
    })

def disconnect_slack_service(id_curso):
    result = disconnect_slack_course(id_curso)

    if not result["ok"]:
        return error_response(result)

    return success_response({
        "message": result["data"]
    })

def get_slack_messages_service(id_curso):
    result = get_slack_messages(id_curso)

    if not result["ok"]:
        return error_response(result)

    return success_response({
        "messages": result["data"]
    })