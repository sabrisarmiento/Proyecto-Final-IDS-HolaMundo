from xmlrpc.server import resolve_dotted_attribute

from flask import jsonify
from database.db import query_db, modify_db

def list_students(name, surname, mail, password, id_rol, created_at):
    try: 
        sql = "SELECT * FROM roles"
        condition = " WHERE 1 = 1"
        params = []

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
    
def create_student(data):
    try: 
        if "nombre" not in data or "apellido" not in data or "correo" not in data or "password" not in data or "id_rol" not in data:
            return jsonify({"errors": [{
                "code": "400", 
                "message": "Bad Request", 
                "level": "error",
                "description": "Faltan campos requeridos: nombre, apellido, correo, password e id_rol"
            }]}), 400
        
        if not isinstance(data["id_rol"], int):
            return jsonify({"errors": [{
                "code": "400", 
                "message": "Bad Request", 
                "level": "error",
                "description": "id_rol debe ser un entero"
            }]}), 400
        
        if not data:
            return jsonify({ "errors": [{
                "code": "400", 
                "message": "Bad Request", 
                "level": "error", 
                "description": "JSON requerido"
            }]}), 400
        
        if data["id_rol"] < 0:
            return jsonify({ "errors": [{
                "code": "400", 
                "message": "Bad Request", 
                "level": "error", 
                "description": "El nivel_administracion debe ser entre 1 y 3"}]}), 400
        
        query_check = """
            SELECT id_alumno FROM alumnos 
            WHERE 1 = 1 
            AND nombre=%s 
            AND apellido=%s
            AND correo=%s
            AND password=%s
            AND id_rol=%s
        """

        existance = query_db(query_check, (
            data["nombre"],
            data["apellido"],
            data["correo"],
            data["password"],
            data["id_rol"]))
        
        if existance:
            return jsonify({ "errors": [{
                "code": "409", 
                "message": "Conflict", 
                "level": "error", 
                "description": "El alumno ya existe"}]}), 409

        query_insert = """
            INSERT INTO alumnos (nombre, apellido, correo, password, id_rol)
            VALUES (%s, %s, %s, %s, %s)
        """

        id_alumno = modify_db(query_insert, (
            data["nombre"],
            data["apellido"],
            data["correo"],
            data["password"],
            data["id_rol"]
        ))

        return jsonify({
            "mensaje": "El alumno ha sido creado exitosamente",
            "id": id_alumno
        }), 201

    except Exception as error:
        return jsonify({"errors": [{
            "code":  "500", 
            "message": "Internal Server Error", 
            "level": "error", 
            "description": str(error)
        }]}), 500