import csv, io
from flask import jsonify
from database.db import query_db, modify_db

_FILTER_COLUMNS = {
    "name": "nombre",
    "surname": "apellido",
    "mail": "mail",
    "password": "password",
    "id_rol": "id_rol",
    "created_at": "created_at",
    "id_curso" : "id_curso",
}

def get_all_students(filters):
    try:
        sql = "SELECT * FROM alumnos WHERE 1 = 1"
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


def get_student_by_id(id):
    try:
        if id <= 0:
            return {"ok": False, "code": 400, "message": "Bad Request",
                    "description": "El ID debe ser un entero positivo mayor a cero."}

        result = query_db("SELECT * FROM alumnos WHERE id_alumno = %s", (id,))
        if not result:
            return {"ok": False, "code": 404, "message": "Not Found",
                    "description": f"No existe un alumno con ID {id}"}
        return {"ok": True, "data": result}
    except Exception as e:
        return {"ok": False, "code": 500, "message": "Internal Server Error",
                "description": str(e)}


def create_student(data):
    try:
        if not data:
            return {"ok": False, "code": 400, "message": "Bad Request",
                    "description": "JSON requerido"}

        required = ["nombre", "apellido", "correo", "password", "id_rol"]
        missing = [k for k in required if k not in data]
        if missing:
            return {"ok": False, "code": 400, "message": "Bad Request",
                    "description": f"Faltan campos: {missing}"}

        if not isinstance(data["id_rol"], int):
            return {"ok": False, "code": 400, "message": "Bad Request",
                    "description": "id_rol debe ser un entero"}
        if data["id_rol"] < 0:
            return {"ok": False, "code": 400, "message": "Bad Request",
                    "description": "id_rol debe ser mayor a 0"}

        exists = query_db(
            "SELECT id_alumno FROM alumnos WHERE correo = %s",
            (data["correo"],),
        )
        if exists:
            return {"ok": False, "code": 409, "message": "Conflict",
                    "description": "El alumno ya existe (correo duplicado)"}

        new_id = modify_db(
            """INSERT INTO alumnos (nombre, apellido, correo, password, id_rol)
            VALUES (%s, %s, %s, %s, %s)""",
            (data["nombre"], data["apellido"], data["correo"],
            data["password"], data["id_rol"]),
        )
        return {"ok": True, "message": "Alumno creado correctamente", "id": new_id}
    except Exception as e:
        return {"ok": False, "code": 500, "message": "Internal Server Error",
                "description": str(e)}


def import_students_from_csv(files):
    if 'file' not in files:
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "No se envió archivo (campo 'file' requerido)"}

    file = files['file']
    if not file.filename.lower().endswith('.csv'):
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "El archivo debe ser .csv"}

    try:
        stream = io.StringIO(file.stream.read().decode("utf-8-sig"), newline=None)
        rows = list(csv.DictReader(stream))
    except Exception as e:
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": f"No se pudo leer el CSV: {e}"}

    if not rows:
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "El CSV está vacío"}

    creados, errores = [], []
    for i, row in enumerate(rows, start=2):
        try:
            row["id_rol"] = int(row["id_rol"])
        except (KeyError, ValueError, TypeError):
            errores.append({"fila": i, "error": "id_rol inválido o ausente"})
            continue

        result = create_student(row)
        if result["ok"]:
            creados.append({"fila": i, "id": result["id"]})
        else:
            errores.append({"fila": i, "status": result["code"],
                            "error": result["description"]})

    status_final = 201 if not errores else (207 if creados else 400)
    return {
        "ok": True,
        "status": status_final,
        "data": {
            "creados": len(creados),
            "errores": len(errores),
            "detalle_creados": creados,
            "detalle_errores": errores,
        },
    }