from flask import jsonify
from database.db import query_db, modify_db
_FILTER_COLUMNS = {
    "id_roles": "id_roles",
    "name": "nombre",
    "admin_level": "nivel_administracion",
}

def get_all_roles(filters):
    admin_level = filters.get("admin_level")
    id_roles = filters.get("id_roles")

    if admin_level is not None and not (1 <= admin_level <= 3):
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "El nivel de administracion tiene que ser de 1 a 3"}

    if id_roles is not None and id_roles <= 0:
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "El id_roles debe ser mayor a 0"}

    try:
        sql = "SELECT * FROM roles WHERE 1 = 1"
        params = []
        for key, column in _FILTER_COLUMNS.items():
            value = filters.get(key)
            if value:
                sql += f" AND {column} = %s"
                params.append(value)
        return {"ok": True, "data": query_db(sql, params)}
    except Exception as e:
        return {"ok": False, "code": 500, "message": "Internal Server Error",
                "description": str(e)}

def create_rol(data):
    if not data:
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "JSON requerido"}

    required = ["nombre", "nivel_administracion"]
    missing = [k for k in required if k not in data]
    if missing:
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": f"Faltan campos requeridos: {', '.join(missing)}"}

    if not isinstance(data["nivel_administracion"], int):
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "nivel_administracion debe ser un entero"}

    if not (1 <= data["nivel_administracion"] <= 3):
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "El nivel_administracion debe ser entre 1 y 3"}

    try:
        exists = query_db(
            "SELECT id_roles FROM roles WHERE nombre = %s AND nivel_administracion = %s",
            (data["nombre"], data["nivel_administracion"]),
        )
        if exists:
            return {"ok": False, "code": 409, "message": "Conflict",
                    "description": "El rol ya existe"}

        rol_id = modify_db(
            "INSERT INTO roles (nombre, nivel_administracion) VALUES (%s, %s)",
            (data["nombre"], data["nivel_administracion"]),
        )
        return {"ok": True, "message": "El rol ha sido creado exitosamente",
                "id": rol_id}
    except Exception as e:
        return {"ok": False, "code": 500, "message": "Internal Server Error",
                "description": str(e)}

def delete_rol_by_id(id):
    if id <= 0:
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "El ID debe ser un entero positivo mayor a cero."}

    try:
        exists = query_db("SELECT id_roles FROM roles WHERE id_roles = %s", (id,))
        if not exists:
            return {"ok": False, "code": 404, "message": "Not Found",
                    "description": "No existe un rol con el ID proporcionado."}

        modify_db("DELETE FROM roles WHERE id_roles = %s", (id,))
        return {"ok": True, "message": f"Rol con ID {id} eliminado correctamente"}
    except Exception as e:
        return {"ok": False, "code": 500, "message": "Internal Server Error",
                "description": str(e)}