from database.db import query_db, modify_db


def get_all_exam_types():
    try:
        result = query_db("SELECT id_tipo, nombre, descripcion FROM tipos_evaluacion")
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


#-----------------------------------------------------------


def get_exam_type_by_id(id):
    try:
        result = query_db(
            "SELECT id_tipo, nombre, descripcion FROM tipos_evaluacion WHERE id_tipo = %s",
            (id,)
        )
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


#-----------------------------------------------------------


def create_exam_type(data):
    try:
        nombre = data.get("nombre")
        descripcion = data.get("descripcion")

        sql = "INSERT INTO tipos_evaluacion (nombre, descripcion) VALUES (%s, %s)"
        new_id = modify_db(sql, (nombre, descripcion))
        return {
            "ok": True,
            "data": new_id
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": str(e)
        }


#-----------------------------------------------------------


def update_exam_type(id, data):
    try:
        existing = query_db(
            "SELECT id_tipo FROM tipos_evaluacion WHERE id_tipo = %s",
            (id,)
        )
        if not existing:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No existe un tipo de evaluación con ID {id}"
            }

        fields = []
        params = []

        if "nombre" in data:
            fields.append("nombre = %s")
            params.append(data["nombre"])
        if "descripcion" in data:
            fields.append("descripcion = %s")
            params.append(data["descripcion"])

        params.append(id)
        sql = f"UPDATE tipos_evaluacion SET {', '.join(fields)} WHERE id_tipo = %s"
        modify_db(sql, params)
        return {
            "ok": True,
            "message": "Tipo de evaluación actualizado con éxito",
            "id_tipo": id
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": str(e)
        }


#-----------------------------------------------------------


def delete_exam_type(id):
    try:
        existing = query_db(
            "SELECT id_tipo FROM tipos_evaluacion WHERE id_tipo = %s",
            (id,)
        )
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
