from flask import Blueprint, request, jsonify
from controller.roles_controller import mostrar_roles

roles_bp = Blueprint('roles', __name__)

@roles_bp.route("/roles", methods = ["GET"])
def list_roles():
    try:
        id_roles = request.args.get('id_roles', -1, type = int)
        nombre = request.args.get('nombre')
        nivel_administracion = request.args.get('nivel_administracion', -1, type = int)

        if nivel_administracion < 1 or nivel_administracion > 3:
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

        lista_buscada = mostrar_roles(id_roles, nombre, nivel_administracion)

        if not lista_buscada:
            return ' ', 204
        
        return jsonify({"roles encontrados"})

    except Exception as error:
        return jsonify({"errors": [{
            "code":  "500", 
            "message": "Internal Server Error", 
            "level": "error", 
            "description": str(error)
        }]}), 500

