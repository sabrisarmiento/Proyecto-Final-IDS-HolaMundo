from flask import Blueprint, request, jsonify
from controller.roles_controller import list_roles, create_rol

roles_bp = Blueprint('roles', __name__)

@roles_bp.route("/roles", methods = ["GET"])
def list_roles_route():
    try:
        id_roles = request.args.get('id_roles', -1, type = int)
        name = request.args.get('nombre')
        admin_level = request.args.get('nivel_administracion', -1, type = int)

        if admin_level < 1 or admin_level > 3:
            return jsonify({"error": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": f"El nivel de administracion tiene que ser de 1 a 3"
            }]}), 400
        
        if id_roles < 0:
            return jsonify({"errors": [{
                    "code": "400", 
                    "message": "Bad request", 
                    "level": "error", 
                    "description": "El id_roles debe ser mayor a 0"
                }]}), 400

        results = list_roles(id_roles, name, admin_level)

        if not results:
            return ' ', 204
        
        return jsonify({"roles encontrados": results})

    except Exception as error:
        return jsonify({"errors": [{
            "code":  "500", 
            "message": "Internal Server Error", 
            "level": "error", 
            "description": str(error)
        }]}), 500

@roles_bp.route("/roles", methods = ["POST"])
def create_roles_route():
    data = request.get_json()
    return create_rol(data)

