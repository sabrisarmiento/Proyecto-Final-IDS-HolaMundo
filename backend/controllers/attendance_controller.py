import math
import hashlib
import os
from dotenv import load_dotenv
from database.db import query_db, modify_db

load_dotenv()

def get_attendance(id_clase=None, id_alumno=None):
    try:
        if id_clase:
            result = query_db("SELECT * FROM asistencia WHERE id_clase = %s", (id_clase,))
        elif id_alumno:
            result = query_db("SELECT * FROM asistencia WHERE id_alumno = %s", (id_alumno,))
        else:
            result = query_db("SELECT * FROM asistencia")
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
    try:
        if not data or "id_alumno" not in data or "id_clase" not in data:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "Los campos 'id_alumno' e 'id_clase' son obligatorios"
            }

        id_alumno = data["id_alumno"]
        id_clase = data["id_clase"]
        code = data.get("code")
        lat = data.get("latitud")
        lon = data.get("longitud")

        expected_code = hashlib.sha256(f"{id_alumno}-{id_clase}-{os.getenv('ATTENDANCE_SECRET')}".encode()).hexdigest()

        if not code or code != expected_code:
            return {
                "ok": False,
                "code": 403,
                "message": "Forbidden",
                "description": "Código QR inválido o ausente"
            }

        if not student_active(id_alumno):

            return {
                "ok": False,
                "code": 403,
                "message": "Forbidden",
                "description": "El alumno figura como abandonó la cursada"
            }

        if lat is None or lon is None:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "Se requiere ubicación GPS para validar asistencia"
            }

        if not proximity_fiuba(float(lat), float(lon)):
            return {
                "ok": False,
                "code": 403,
                "message": "Forbidden",
                "description": "Ubicación fuera del rango permitido"
            }

        sql = "INSERT INTO asistencia (id_alumno, id_clase, presente) VALUES (%s, %s, %s)"
        modify_db(sql, (data["id_alumno"], data["id_clase"], data.get("presente", True)))
        return {
            "ok": True,
            "message": "Asistencia registrada correctamente"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": str(e)
        }

def update_attendance(id, data):
    try:
        if id <= 0:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "El ID debe ser un número entero positivo"
            }

        if not data or "presente" not in data:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "El campo 'presente' es obligatorio"
            }

        if not isinstance(data["presente"], bool):
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "El campo 'presente' debe ser un booleano"
            }

        existing = query_db("SELECT id_asistencia FROM asistencia WHERE id_asistencia = %s", (id,))
        if not existing:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No existe un registro de asistencia con ID {id}"
            }

        modify_db("UPDATE asistencia SET presente = %s WHERE id_asistencia = %s", (data["presente"], id))
        return {
            "ok": True,
            "message": "Asistencia actualizada con éxito"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": str(e)
        }

def delete_attendance(id):
    try:
        if id <= 0:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "El ID debe ser un número entero positivo"
            }

        existing = query_db("SELECT id_asistencia FROM asistencia WHERE id_asistencia = %s", (id,))
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
            "message": f"Registro de asistencia con ID {id} eliminado correctamente"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }
