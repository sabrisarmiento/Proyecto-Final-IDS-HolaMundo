from flask import Blueprint, request, jsonify
from services.rol_service import (
    roles_service,
    create_rol_service,
    delete_rol_service,
)
from middleware.auth_middleware import require_auth, require_min_admin_level
from helpers.constants import NIVEL_SUPERADMIN

roles_bp = Blueprint('roles', __name__)

@roles_bp.route("/roles", methods = ["GET"])
@require_auth
def list_roles_route():
    filters = {
        "id_roles": request.args.get("id_roles", type=int),
        "name": request.args.get("name"),
        "admin_level": request.args.get("admin_level", type=int),
    }
    return roles_service(filters)


@roles_bp.route("/roles", methods=["POST"])
@require_auth
@require_min_admin_level(NIVEL_SUPERADMIN)
def create_rol_route():
    return create_rol_service(request.get_json(silent=True))


@roles_bp.route("/roles/<int:id>", methods=["DELETE"])
@require_auth
@require_min_admin_level(NIVEL_SUPERADMIN)
def delete_rol_route(id):
    return delete_rol_service(id)