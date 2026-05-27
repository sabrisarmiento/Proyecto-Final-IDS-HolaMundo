from helpers.responses import error_response, success_response
from controllers.calendar_controller import (
    get_all_events, create_event, get_event_by_id, patch_event_by_id, delete_event_by_id
)

def calendar_list_service(filters):
    result = get_all_events(filters)
    
    return success_response({"events": result["data"]}) if result["ok"] else error_response(result)

def create_calendar_service(data):
    result = create_event(data)
    return success_response({"message": result["message"]}, 201) if result["ok"] else error_response(result)

def get_calendar_event_service(id_event):
    result = get_event_by_id(id_event)
    return success_response({"event": result["data"]}) if result["ok"] else error_response(result)

def patch_calendar_service(id_event, data):
    result = patch_event_by_id(id_event, data)
    return success_response({"message": result["message"]}) if result["ok"] else error_response(result)

def delete_calendar_service(id_event):
    result = delete_event_by_id(id_event)
    return success_response({"message": result["message"]}) if result["ok"] else error_response(result)