import math
from database.db import query_db, modify_db

def get_attendance(id_clase=None, id_alumno=None):
    if id_clase:
        return query_db("SELECT * FROM asistencia WHERE id_clase = %s", (id_clase,))
    if id_alumno:
        return query_db("SELECT * FROM asistencia WHERE id_alumno = %s", (id_alumno,))
    return query_db("SELECT * FROM asistencia")

def student_active(id_alumno):
    sql = "SELECT estado_alumno FROM alumnos WHERE id_alumno = %s"
    result = query_db(sql, (id_alumno,))
    return result[0]['estado_alumno'] if result else False

def students_active_qr(id_clase):
    try:
        sql = """
            SELECT a.id_alumno, a.correo, a.nombre, a.apellido 
            FROM alumnos a
            WHERE a.id_curso = (SELECT id_curso FROM clases WHERE id_clase = %s) 
            AND a.estado_alumno = 1
        """
        return query_db(sql, (id_clase,))
    except Exception:
        return []

def proximity_fiuba(user_lat, user_lon):
    FACULTAD_LAT = -34.61771131976023 
    FACULTAD_LON = -58.36825700810214
    RADIO_PERMITIDO_METROS = 300

    dlat = math.radians(user_lat - FACULTAD_LAT)
    dlon = math.radians(user_lon - FACULTAD_LON)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(FACULTAD_LAT)) * math.cos(math.radians(user_lat)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distancia = 6371 * c * 1000 
    
    return distancia <= RADIO_PERMITIDO_METROS

def create_attendance(data):
    query = "INSERT INTO asistencia (id_alumno, id_clase, presente) VALUES (%s, %s, %s)"
    return modify_db(query, (data["id_alumno"], data["id_clase"], data.get("presente", True)))

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
