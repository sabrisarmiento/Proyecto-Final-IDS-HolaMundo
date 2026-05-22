from flask import Blueprint, request, jsonify
from services.rol_service import handle_list_roles, handle_create_rol, handle_delete_rol

roles_bp = Blueprint('roles', __name__)

@roles_bp.route("/roles", methods = ["GET"])
def list_roles_route():
    filters = {
        "id_roles": request.args.get("id_roles", type=int),
        "name": request.args.get("name"),
        "admin_level": request.args.get("admin_level", type=int),
    }
    return handle_list_roles(filters)

@roles_bp.route("/roles", methods=["POST"])
def create_rol_route():
    return handle_create_rol(request.get_json(silent=True))

@roles_bp.route("/roles/<int:id>", methods=["DELETE"])
def delete_rol_route(id):
    return handle_delete_rol(id)