import csv, io
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
        if not data:
            return {"error": "JSON requerido"}, 400
        
        required = ["nombre", "apellido", "correo", "password", "id_rol"]
        missing = [k for k in required if k not in data]
        if missing:
            return {"error": f"Faltan campos: {missing}"}, 400
        
        if not isinstance(data["id_rol"], int):
            return {"error": "id_rol debe ser un entero"}, 400
        
        if data["id_rol"] < 0:
            return {"error": "id_rol debe ser mayor a 0"}, 400
        
        query_check = """
            SELECT id_alumno FROM alumnos
            WHERE correo = %s
        """
        if query_db(query_check, (data["correo"],)):
            return {"error": "El alumno ya existe (correo duplicado)"}, 409

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

        return {"id": id_alumno, "mensaje": "creado"}, 201

    except Exception as error:
        return {"error": str(error)}, 500
    
def import_students(files):
    if 'file' not in files:
        return jsonify({"errors": [{
            "code": "400", 
            "message": "Bad Request", 
            "level": "error",
            "description": "No se envió archivo (campo 'file' requerido)"
        }]}), 400
    
    file = files['file']

    if not file.filename.lower().endswith('.csv'):
        return jsonify({"errors": [{
            "code": "400", "message": "Bad Request", "level": "error",
            "description": "El archivo debe ser .csv"
        }]}), 400
    
    try: 
        stream = io.StringIO(file.stream.read().decode("utf-8-sig"), newline=None)
        reader = csv.DictReader(stream)
        rows = list(reader)

    except Exception as e:
        return jsonify({"errors": [{
            "code": "400", "message": "Bad Request", "level": "error",
            "description": f"No se pudo leer el CSV: {e}"
        }]}), 400

    if not rows:
        return jsonify({"errors": [{
            "code": "400", "message": "Bad Request", "level": "error",
            "description": "El CSV está vacío"
        }]}), 400
    
    creados = []
    errores = []

    for i, row in enumerate(rows, start=2):
        try:
            row["id_rol"] = int(row["id_rol"])
        except (KeyError, ValueError, TypeError):
            errores.append({"fila": i, "error": "id_rol inválido o ausente"})
            continue

        result, status = create_student(row)

        if status == 201:
            creados.append({"fila": i, "id": result["id"]})
        else:
            errores.append({"fila": i, "status": status, "error": result.get("error")})

    status_final = 201 if not errores else (207 if creados else 400)
    return jsonify({
        "creados": len(creados),
        "errores": len(errores),
        "detalle_creados": creados,
        "detalle_errores": errores
    }), status_final