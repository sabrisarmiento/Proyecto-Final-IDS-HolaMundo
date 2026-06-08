from database.db import query_db, modify_db

def add_student_to_team(data):
    try:
        id_equipo = data.get("id_equipo")
        padron = data.get("padron")
        forzar = data.get("forzar", False)
        if not id_equipo or not padron:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "id_equipo y id_alumno son obligatorios"
            }
        alumno = query_db( """ SELECT id_alumno FROM alumnos WHERE padron = %s """, (padron,))
        if not alumno:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": "No existe un alumno con ese padrón"
            }
        id_alumno = alumno[0]["id_alumno"]
        existe = query_db(
            """ 
            SELECT ea.id_equipo, e.nombre_equipo 
            FROM equipo_alumno ea
            JOIN equipos e ON ea.id_equipo = e.id_equipo
            WHERE ea.id_alumno = %s 
            """, (id_alumno,)
        )
        if existe:
            nombre_equipo = existe[0]["nombre_equipo"]
            if not forzar:
                return {
                    "ok": False,
                    "code": 409,
                    "message": "Conflict",
                    "description": f"El alumno ya pertenece al equipo '{nombre_equipo}'"
                }
            modify_db(""" DELETE FROM equipo_alumno WHERE id_alumno = %s """, (id_alumno,))
        modify_db(""" INSERT INTO equipo_alumno (id_equipo, id_alumno) VALUES (%s, %s) """, (id_equipo, id_alumno))
        return {
            "ok": True,
            "message": "Alumno agregado al equipo"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }

def remove_student_from_team(data):
    try:
        id_equipo = data.get("id_equipo")
        id_alumno = data.get("id_alumno")
        modify_db(""" DELETE FROM equipo_alumno WHERE id_equipo = %s AND id_alumno = %s """, (id_equipo, id_alumno))
        return {
            "ok": True,
            "message": "Alumno removido del equipo"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }