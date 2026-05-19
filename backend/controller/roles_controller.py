from flask import jsonify
from database.db import query_db, modify_db
def list_roles(id_roles, name, admin_level):
    sql = "SELECT * FROM roles"
    condition = " WHERE 1 = 1"
    params = []

    if id_roles:
        condition += " AND id_roles = %s"
        params.append(id_roles)

    if name:
        condition += " AND nombre = %s"
        params.append(name)
    
    if admin_level:
        condition += " AND nivel_administracion = %s"
        params.append(admin_level)
    
    return query_db(sql + condition, params)

def create_rol(data):
    try:
        if not data:
            return jsonify({ "errors": [{
                "code": "400", 
                "message": "Bad Request", 
                "level": "error", 
                "description": "JSON requerido"
            }]}), 400
        
        if data["nivel_administracion"] > 3 or data["nivel_administracion"] < 1:
            return jsonify({ "errors": [{
                "code": "400", 
                "message": "Bad Request", 
                "level": "error", 
                "description": "El nivel_administracion debe ser entre 1 y 3"}]}), 400
        
        query_check = """
            SELECT id_roles FROM roles 
            WHERE 1 = 1 AND nombre=%s AND nivel_administracion=%s
        """

        existance = query_db(query_check, (
            data["nombre"],
            data["nivel_administracion"]
        ))

        if existance:
            return jsonify({ "errors": [{
                "code": "409", 
                "message": "Conflict", 
                "level": "error", 
                "description": "El rol ya existe"}]}), 409
        
        query_insert = """
            INSERT INTO roles (nombre, nivel_administracion)
            VALUES (%s, %s)
        """

        rol_id = modify_db(query_insert, (
            data["nombre"],
            data["nivel_administracion"]
        ))

        return jsonify({
            "mensaje": "El rol ha sido creado exitosamente",
            "id": rol_id
        }), 201
    
    except Exception as e:
        return jsonify({ "errors": [{
            "code": "500", 
            "message": "Internal Server Error", 
            "level": "error", 
            "description": str(e)}]}), 500
    
def delete_rol(id):
    query_check = "SELECT * FROM roles WHERE id_roles = %s"
    existance = query_db(query_check, (id, ))

    if not existance:
        return jsonify({"errors": [{
                    "code": "NOT_FOUND",
                    "message": "id_rol no encontrado",
                    "level": "error",
                    "description": "No existe un rol con el ID proporcionado."
                }]}), 404
    
    query_delete = "DELETE FROM roles WHERE id_roles = %s"

    modify_db(query_delete, (id, ))

    return '', 204
