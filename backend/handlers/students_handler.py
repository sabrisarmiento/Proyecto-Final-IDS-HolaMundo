import csv, io
from flask import jsonify
from controller.students_controller import (
    fetch_students,
    fetch_student_by_id,
    insert_student,
    student_exists_by_email,
)

def _error(code, message, description, status):
    return jsonify({"errors": [{
        "code": code,
        "message": message,
        "level": "error",
        "description": description,
    }]}), status

def handle_list_students(filters):
    try:
        results = fetch_students(filters)
        if not results:
            return "", 204
        return jsonify(results), 200
    except Exception as e:
        return _error("500", "Internal Server Error", str(e), 500)
    
def handle_search_student_by_id(id):
    if id <= 0:
        return _error(
            "BAD_REQUEST", "ID inválido",
            "El ID debe ser un número entero positivo mayor a cero.", 400
        )
    try:
        student = fetch_student_by_id(id)
        if not student:
            return _error(
                "NOT_FOUND", "Alumno no encontrado",
                "No existe un alumno con el ID proporcionado.", 404
            )
        return jsonify(student), 200
    except Exception as e:
        return _error("500", "Internal Server Error", str(e), 500)


def handle_create_student(data):
    if not data:
        return jsonify({"error": "JSON requerido"}), 400

    required = ["nombre", "apellido", "correo", "password", "id_rol"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Faltan campos: {missing}"}), 400

    if not isinstance(data["id_rol"], int):
        return jsonify({"error": "id_rol debe ser un entero"}), 400
    if data["id_rol"] < 0:
        return jsonify({"error": "id_rol debe ser mayor a 0"}), 400

    try:
        if student_exists_by_email(data["correo"]):
            return jsonify({"error": "El alumno ya existe (correo duplicado)"}), 409

        new_id = insert_student(data)
        return jsonify({"id": new_id, "mensaje": "creado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def handle_import_students(files):
    if "file" not in files:
        return _error("400", 
    "Bad Request",
    "No se envió archivo (campo 'file' requerido)", 400)

    file = files["file"]
    if not file.filename.lower().endswith(".csv"):
        return _error("400", "Bad Request", "El archivo debe ser .csv", 400)

    try:
        stream = io.StringIO(file.stream.read().decode("utf-8-sig"), newline=None)
        rows = list(csv.DictReader(stream))
    except Exception as e:
        return _error("400", "Bad Request", f"No se pudo leer el CSV: {e}", 400)

    if not rows:
        return _error("400", "Bad Request", "El CSV está vacío", 400)

    creados, errores = [], []
    for i, row in enumerate(rows, start=2):
        try:
            row["id_rol"] = int(row["id_rol"])
        except (KeyError, ValueError, TypeError):
            errores.append({"fila": i, "error": "id_rol inválido o ausente"})
            continue

        response, status = handle_create_student(row)
        body = response.get_json()
        if status == 201:
            creados.append({"fila": i, "id": body["id"]})
        else:
            errores.append({"fila": i, "status": status, "error": body.get("error")})

    status_final = 201 if not errores else (207 if creados else 400)
    return jsonify({
        "creados": len(creados),
        "errores": len(errores),
        "detalle_creados": creados,
        "detalle_errores": errores,
    }), status_final