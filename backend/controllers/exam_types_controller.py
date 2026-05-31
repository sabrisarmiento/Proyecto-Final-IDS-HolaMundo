from database.db import query_db, modify_db

def get_all_exam_types():
    try:
        result = query_db("SELECT * FROM tipos_evaluacion")
        return {
            "ok": True,
            "data": result
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }

def get_exam_type_by_id(id):
    try:
        if id <= 0:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "El ID debe ser un número entero positivo"
            }

        result = query_db("SELECT * FROM tipos_evaluacion WHERE id_tipo = %s", (id,))
        if not result:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No existe un tipo de evaluación con ID {id}"
            }
        return {
            "ok": True,
            "data": result[0]
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }

def create_exam_type(data):
    try:
        if not data or "nombre" not in data:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "El campo 'nombre' es obligatorio"
            }

        sql = "INSERT INTO tipos_evaluacion (nombre, descripcion) VALUES (%s, %s)"
        modify_db(sql, (data["nombre"], data.get("descripcion")))
        return {
            "ok": True,
            "message": "Tipo de evaluación creado correctamente"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": str(e)
        }

def update_exam_type(id, data):
    try:
        if id <= 0:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "El ID debe ser un número entero positivo"
            }

        if not data:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "Debe enviar al menos un campo para actualizar"
            }

        campos_validos = {"nombre", "descripcion"}
        for campo in data:
            if campo not in campos_validos:
                return {
                    "ok": False,
                    "code": 400,
                    "message": "Bad Request",
                    "description": f"El campo '{campo}' no es válido"
                }

        existing = query_db("SELECT id_tipo FROM tipos_evaluacion WHERE id_tipo = %s", (id,))
        if not existing:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No existe un tipo de evaluación con ID {id}"
            }

        fields = []
        values = []
        if "nombre" in data:
            fields.append("nombre = %s")
            values.append(data["nombre"])
        if "descripcion" in data:
            fields.append("descripcion = %s")
            values.append(data["descripcion"])

        values.append(id)
        modify_db(f"UPDATE tipos_evaluacion SET {', '.join(fields)} WHERE id_tipo = %s", values)
        return {
            "ok": True,
            "message": "Tipo de evaluación actualizado con éxito"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": str(e)
        }

def delete_exam_type(id):
    try:
        if id <= 0:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "El ID debe ser un número entero positivo"
            }

        existing = query_db("SELECT id_tipo FROM tipos_evaluacion WHERE id_tipo = %s", (id,))
        if not existing:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No existe un tipo de evaluación con ID {id}"
            }

        modify_db("DELETE FROM tipos_evaluacion WHERE id_tipo = %s", (id,))
        return {
            "ok": True,
            "message": f"Tipo de evaluación con ID {id} eliminado correctamente"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }
