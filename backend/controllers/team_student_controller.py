from database.db import query_db, modify_db

def add_student_to_team(data):
    try:
        id_equipo = data.get("id_equipo")
        id_alumno = data.get("id_alumno")
        if not id_equipo or not id_alumno:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "id_equipo y id_alumno son obligatorios"
            }
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
            return {
                "ok": False,
                "code": 409,
                "message": "Conflict",
                "description": f"El alumno ya pertenece al equipo '{nombre_equipo}'"
            }
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