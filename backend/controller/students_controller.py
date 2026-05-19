from xmlrpc.server import resolve_dotted_attribute

from flask import jsonify
from database.db import query_db, modify_db

def list_students(id_alumnos, name, surname, mail, password, id_rol, created_at):
    try: 
        sql = "SELECT * FROM roles"
        condition = " WHERE 1 = 1"
        params = []

        if id_alumnos is not None and id_alumnos <= 0:
            return jsonify({"errors": [{
                    "code": "400", 
                    "message": "Bad request", 
                    "level": "errors", 
                    "description": "El id_alumnos debe ser mayor a 0"
                }]}), 400

        if id_alumnos:
            condition += " AND id_alumnos = %s"
            params.append(id_alumnos)
        
        if name:
            condition += " AND nombre = %s"
            params.append(name)
        
        if surname:
            condition += " AND apellido = %s"
            params.append(surname)
        
        if mail:
            condition += " AND mail = %s"
            params.append(mail)
    
        if password:
            condition += " AND password = %s"
            params.append(password)
        
        if id_rol:
            condition += " AND id_rol = %s"
            params.append(id_rol)
        
        if created_at:
            condition += " AND created_at = %s"
            params.append(created_at)
        
        results = query_db(sql + condition, params)

        if not results:
            return '', 204
        
        return results

    except Exception as error:
        return jsonify({"errors": [{
            "code":  "500", 
            "message": "Internal Server Error", 
            "level": "errors", 
            "description": str(error)
        }]}), 500
    
def search_student_by_id(id):
    if id <= 0:
        return jsonify({"errors": [{
                "code": "BAD_REQUEST",
                "message": "ID inválido",
                "level": "error",
                "description": "El ID debe ser un número entero positivo mayor a cero."
            }]}), 400
    
    try:
        query_check = "SELECT * FROM roles WHERE id_roles = %s"
        existance = query_db(query_check, (id, ))

        if not existance:
            return jsonify({"errors": [{
                    "code": "NOT_FOUND",
                    "message": "id_rol no encontrado",
                    "level": "error",
                    "description": "No existe un rol con el ID proporcionado."
                }]}), 404

        return existance

    except Exception as error:
        return jsonify({"errors": [{
            "code":  "500", 
            "message": "Internal Server Error", 
            "level": "error", 
            "description": str(error)
        }]}), 500