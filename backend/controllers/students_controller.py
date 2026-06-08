import csv, io
from database.db import query_db, modify_db

_FILTER_COLUMNS = {
    "name": "nombre",
    "surname": "apellido",
    "padron": "padron",
    "mail": "correo",
    "id_course": "id_curso",
    "id_curso" : "id_curso",
    "state_student": "estado_alumno",
}

def get_all_students(filters):
    try:
        limit = filters.pop('limit', None)
        offset = filters.pop('offset', 0)

        sql = "SELECT * FROM alumnos WHERE 1 = 1"
        count_sql = "SELECT COUNT(*) as total FROM alumnos WHERE 1 = 1"
        params = []

        for key, column in _FILTER_COLUMNS.items():
            value = filters.get(key)
            if value:
                condition = f" AND {column} = %s"
                sql += condition
                count_sql += condition
                params.append(value)

        order_by = filters.get("order_by", None)
        order = filters.pop("order", None)

        if order_by and order:
            sql += f" ORDER BY {order_by} {order.upper()}"

        total = query_db(count_sql, params)[0]['total']

        if limit is not None:
            sql += " LIMIT %s OFFSET %s"
            params.append(int(limit))
            params.append(int(offset))

        return {"ok": True, "data": query_db(sql, params), "total": total}
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

        required = ["nombre", "apellido", "padron", "correo", "id_curso"]
        missing = [k for k in required if k not in data]
        if missing:
            return {"ok": False, "code": 400, "message": "Bad Request",
                    "description": f"Faltan campos: {missing}"}

        exists = query_db(
            "SELECT id_alumno FROM alumnos WHERE correo = %s OR padron = %s",
            (data["correo"], data["padron"]),
        )
        if exists:
            return {"ok": False, "code": 409, "message": "Conflict",
                    "description": "El alumno ya existe (correo o padrón duplicado)"}

        new_id = modify_db(
            """INSERT INTO alumnos (nombre, apellido, padron, correo, id_curso)
            VALUES (%s, %s, %s, %s, %s)""",
            (data["nombre"], data["apellido"], data["padron"], data["correo"], data["id_curso"]),
        )
        return {"ok": True, "message": "Alumno creado correctamente", "id": new_id}
    except Exception as e:
        return {"ok": False, "code": 500, "message": "Internal Server Error",
                "description": str(e)}


COLUMNAS_CSV = ["nombre", "apellido", "padron", "mail"]


def import_students_from_csv(files, id_curso):
    if 'file' not in files:
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "No se envió archivo (campo 'file' requerido)"}

    file = files['file']
    if not file.filename.lower().endswith('.csv'):
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "El archivo debe ser .csv"}

    if id_curso in (None, ""):
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "Falta el id_curso (en form-data o query param)"}
    try:
        id_curso = int(id_curso)
    except (ValueError, TypeError):
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "El id_curso debe ser un entero"}

    try:
        stream = io.StringIO(file.stream.read().decode("utf-8-sig"), newline=None)
        reader = csv.DictReader(stream)
        recibidas = [h.strip() for h in (reader.fieldnames or [])]
        rows = list(reader)
    except Exception as e:
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": f"No se pudo leer el CSV: {e}"}

    # Validación estricta de columnas: exactamente las de COLUMNAS_CSV
    faltantes = [c for c in COLUMNAS_CSV if c not in recibidas]
    sobrantes = [c for c in recibidas if c not in COLUMNAS_CSV]
    if faltantes or sobrantes:
        partes = []
        if faltantes:
            partes.append(f"faltan columnas: {faltantes}")
        if sobrantes:
            partes.append(f"columnas no permitidas: {sobrantes}")
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "El CSV debe tener exactamente las columnas "
                               f"{COLUMNAS_CSV}. " + "; ".join(partes)}

    if not rows:
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "El CSV no tiene filas de datos"}

    creados, errores = [], []
    for i, row in enumerate(rows, start=2):
        nombre = (row.get("nombre") or "").strip()
        apellido = (row.get("apellido") or "").strip()
        padron = (row.get("padron") or "").strip()
        correo = (row.get("mail") or "").strip()

        if not all([nombre, apellido, padron, correo]):
            errores.append({"fila": i, "error": "Hay campos vacíos en la fila"})
            continue
        try:
            padron = int(padron)
        except (ValueError, TypeError):
            errores.append({"fila": i, "error": "padron inválido (debe ser numérico)"})
            continue

        result = create_student({
            "nombre": nombre,
            "apellido": apellido,
            "padron": padron,
            "correo": correo,
            "id_curso": id_curso,
        })
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