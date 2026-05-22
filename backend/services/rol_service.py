from flask import jsonify
from controllers.roles_controller import (
    fetch_roles,
    fetch_rol_by_id,
    rol_exists,
    insert_rol,
    delete_rol_by_id,
)

def _error(code, message, description, status):
    return jsonify({"errors": [{
        "code": code,
        "message": message,
        "level": "error",
        "description": description,
    }]}), status


def handle_list_roles(filters):
    admin_level = filters.get("admin_level")
    id_roles = filters.get("id_roles")

    if admin_level is not None and not (1 <= admin_level <= 3):
        return _error("400", "Bad Request",
    "El nivel de administracion tiene que ser de 1 a 3", 400)

    if id_roles is not None and id_roles <= 0:
        return _error("400", "Bad Request",
    "El id_roles debe ser mayor a 0", 400)

    try:
        results = fetch_roles(filters)
        if not results:
            return "", 204
        return jsonify({"roles encontrados": results}), 200
    except Exception as e:
        return _error("500", "Internal Server Error", str(e), 500)


def handle_create_rol(data):
    if not data:
        return _error("400", "Bad Request", "JSON requerido", 400)

    required = ["nombre", "nivel_administracion"]
    missing = [k for k in required if k not in data]
    if missing:
        return _error("400", "Bad Request",
    f"Faltan campos requeridos: {', '.join(missing)}", 400)

    if not isinstance(data["nivel_administracion"], int):
        return _error("400", "Bad Request",
    "nivel_administracion debe ser un entero", 400)

    if not (1 <= data["nivel_administracion"] <= 3):
        return _error("400", "Bad Request",
    "El nivel_administracion debe ser entre 1 y 3", 400)

    try:
        if rol_exists(data["nombre"], data["nivel_administracion"]):
            return _error("409", "Conflict", "El rol ya existe", 409)

        rol_id = insert_rol(data)
        return jsonify({
            "mensaje": "El rol ha sido creado exitosamente",
            "id": rol_id,
        }), 201
    except Exception as e:
        return _error("500", "Internal Server Error", str(e), 500)


def handle_delete_rol(id):
    if id <= 0:
        return _error("BAD_REQUEST", "ID inválido",
    "El ID debe ser un número entero positivo mayor a cero.", 400)

    try:
        if not fetch_rol_by_id(id):
            return _error("NOT_FOUND", "id_rol no encontrado",
    "No existe un rol con el ID proporcionado.", 404)

        delete_rol_by_id(id)
        return "", 204
    except Exception as e:
        return _error("500", "Internal Server Error", str(e), 500)