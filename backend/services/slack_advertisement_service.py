# from helpers.responses import success_response, error_response
# from controllers.slack_advertisement_controller import get_slack_advertisements

# def slack_advertisements_service():
#     result = get_slack_advertisements()

#     if not result["ok"]:
#         return error_response(result)

#     return success_response({
#         "advertisements": result["data"]
#   })