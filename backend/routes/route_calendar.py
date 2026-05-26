from flask import Blueprint, request
from services.calendar_service import (
    calendar_list_service, create_calendar_service, get_calendar_event_service,
    patch_calendar_service, delete_calendar_service
)

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/calendario', methods=['GET'])
def get_calendar():
    filters = {
        "id_profesor": request.args.get('id_profesor'),
        "fecha_evento": request.args.get('fecha_evento'),
        "tipo_clase": request.args.get('tipo_clase')
    }
    return calendar_list_service(filters)

@calendar_bp.route('/calendario/<int:id_event>', methods=['GET'])
def get_event(id_event):
    return get_calendar_event_service(id_event)

@calendar_bp.route('/calendario', methods=['POST'])
def create_event_route():
    data = request.get_json()
    return create_calendar_service(data)

@calendar_bp.route('/calendario/<int:id_event>', methods=['PATCH'])
def patch_event_route(id_event):
    data = request.get_json()
    return patch_calendar_service(id_event, data)

@calendar_bp.route('/calendario/<int:id_event>', methods=['DELETE'])
def delete_event_route(id_event):
    return delete_calendar_service(id_event)