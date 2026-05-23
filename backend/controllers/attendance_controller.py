from database.db import query_db, modify_db


def get_all_attendance(filters):
    try:
        id_clase = filters.get("id_clase")
        id_alumno = filters.get("id_alumno")

        sql = "SELECT id_asistencia, id_alumno, id_clase, presente FROM asistencia"
        condition = " WHERE 1=1"
        params = []

        if id_clase is not None:
            condition += " AND id_clase = %s"
            params.append(int(id_clase))
        if id_alumno is not None:
            condition += " AND id_alumno = %s"
            params.append(int(id_alumno))

        result = query_db(sql + condition, params)
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


def create_attendance(data):
    try:
        id_alumno = data.get("id_alumno")
        id_clase = data.get("id_clase")
        presente = data.get("presente", False)

        sql = "INSERT INTO asistencia (id_alumno, id_clase, presente) VALUES (%s, %s, %s)"
        new_id = modify_db(sql, (id_alumno, id_clase, presente))
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


def update_attendance(id, data):
    try:
        existing = query_db(
            "SELECT id_asistencia FROM asistencia WHERE id_asistencia = %s",
            (id,)
        )
        if not existing:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No existe un registro de asistencia con ID {id}"
            }

        modify_db(
            "UPDATE asistencia SET presente = %s WHERE id_asistencia = %s",
            (data["presente"], id)
        )
        return {
            "ok": True,
            "message": "Asistencia actualizada con éxito",
            "id_asistencia": id
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": str(e)
        }


#-----------------------------------------------------------


def delete_attendance(id):
    try:
        existing = query_db(
            "SELECT id_asistencia FROM asistencia WHERE id_asistencia = %s",
            (id,)
        )
        if not existing:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No existe un registro de asistencia con ID {id}"
            }
        modify_db("DELETE FROM asistencia WHERE id_asistencia = %s", (id,))
        return {
            "ok": True,
            "message": f"Asistencia con ID {id} eliminada correctamente"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }
