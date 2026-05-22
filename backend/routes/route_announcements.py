from flask import Blueprint, app, request
from controllers.announcements_controller import get_announcement_by_id, get_announcements

announcements_bp = Blueprint('announcements', __name__)

@announcements_bp.route('/announcements', methods=['GET'])
def get_announcements_route():
        return get_announcements()

@announcements_bp.route('/announcements/<id>', methods=['GET'])
def get_announcement_by_id_route(id):
        return get_announcement_by_id(id)                

@announcements_bp.route('/announcements', methods=['POST'])
def create_announcement():
        return "Crear anuncio"

@announcements_bp.route('/announcements/<id>', methods=['PATCH'])
def update_announcement(id):
        return f"Actualizar anuncio con id {id}"

@announcements_bp.route('/announcements/<id>', methods=['DELETE'])
def delete_announcement(id):
        return f"Eliminar anuncio con id {id}"  