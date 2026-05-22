from database.db import query_db, modify_db

def get_attendance(id_clase=None, id_alumno=None):
    if id_clase:
        return query_db("SELECT * FROM asistencia WHERE id_clase = %s", (id_clase,))
    if id_alumno:
        return query_db("SELECT * FROM asistencia WHERE id_alumno = %s", (id_alumno,))
    return query_db("SELECT * FROM asistencia")

def create_attendance(data):
    query = "INSERT INTO asistencia (id_alumno, id_clase, presente) VALUES (%s, %s, %s)"
    return modify_db(query, (data["id_alumno"], data["id_clase"], data.get("presente", False)))

def update_attendance(id, presente):
    result = query_db("SELECT id_asistencia FROM asistencia WHERE id_asistencia = %s", (id,))
    if not result:
        return False
    modify_db("UPDATE asistencia SET presente = %s WHERE id_asistencia = %s", (presente, id))
    return True

def delete_attendance(id):
    result = query_db("SELECT id_asistencia FROM asistencia WHERE id_asistencia = %s", (id,))
    if not result:
        return False
    modify_db("DELETE FROM asistencia WHERE id_asistencia = %s", (id,))
    return True
