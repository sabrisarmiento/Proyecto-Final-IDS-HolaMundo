from controllers.slack_controller import configure_slack_course, get_slack_messages, disconnect_slack_course
from helpers.responses import error_response, success_response

# def install_slack_service(id_curso, user):
#     url = build_slack_install_url(id_curso, user)
#     return redirect(url)


# def slack_oauth_callback_service(code, state, error=None):
#     if error:
#         id_curso = None

#         if state and ":" in state:
#             id_curso = state.split(":")[0]

#         if id_curso:
#             return redirect(f"http://127.0.0.1:5001/cursos/{id_curso}?tab=ads&slack=cancelled")

#         return redirect("http://127.0.0.1:5001/cursos?slack=cancelled")
    
#     result = handle_slack_callback(code, state)

#     if not result["ok"]:
#         return error_response(result)

#     return redirect(f"http://localhost:5001/cursos/{result['id_curso']}?tab=ads")

def configure_slack_course_service(id_curso, data, user):
    id_usuario = user["id_usuario"]

    result = configure_slack_course(id_curso, data, id_usuario)

    if not result["ok"]:
        return error_response(result)

    return success_response({
        "message": result["data"]
    })


# def get_slack_advertisements_service(id_curso):
#     result = get_slack_advertisements(id_curso)

#     if not result["ok"]:
#         return error_response(result)

#     return success_response({
#         "advertisements": result["data"]
#     })

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