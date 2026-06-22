from database.db import query_db, modify_db

def get_all_courses(filters):
    try:
        materia = filters.get('materia')
        catedra = filters.get('catedra')
        year = filters.get('anio')

        sql = """
            SELECT 
                c.id_curso,
                m.nombre AS materia,
                c.catedra,
                c.cuatrimestre,
                c.anio,
                c.slack_url,
                c.youtube_url,
                c.regimen_aprobacion
            FROM cursos c
            JOIN materias m ON c.id_materia = m.id_materia
        """
        condition = " WHERE 1=1"
        params = []

        if materia:
            condition += " AND m.nombre LIKE %s"
            params.append(f"%{materia}%")

        if catedra:
            condition += " AND c.catedra LIKE %s"
            params.append(f"%{catedra}%")

        if year:
            condition += " AND c.anio = %s"
            params.append(int(year))

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

def get_courses_for_user(id_user, is_admin, filters):
    try:
        if is_admin:
            return get_all_courses(filters)   # superadmin ve todo

        sql = """
            SELECT c.id_curso, m.nombre AS materia, c.catedra, c.cuatrimestre, c.anio, c.slack_url, c.youtube_url
            FROM cursos c
            JOIN materias m ON c.id_materia = m.id_materia
        """
        condition = """
            WHERE (c.id_profesor = %s
            OR c.id_curso IN (SELECT id_curso FROM curso_ayudantes WHERE id_usuario = %s))
        """
        params = [id_user, id_user]

        if filters.get('materia'):
            condition += " AND m.nombre LIKE %s"; params.append(f"%{filters['materia']}%")
        if filters.get('catedra'):
            condition += " AND c.catedra LIKE %s"; params.append(f"%{filters['catedra']}%")
        if filters.get('anio'):
            condition += " AND c.anio = %s"; params.append(int(filters['anio']))

        return {"ok": True, "data": query_db(sql + condition, params)}
    except Exception as e:
        return {"ok": False, "code": 500, "message": "Internal Server Error", "description": str(e)}


def get_course_id(id_course):
    try:
        sql = """
            SELECT c.id_curso, m.nombre AS materia, c.catedra, c.cuatrimestre, c.anio, c.slack_url, c.youtube_url, c.regimen_aprobacion,
            u.id_usuario AS profesor_id, u.nombre AS profesor_nombre, u.apellido AS profesor_apellido
            FROM cursos c
            JOIN materias m ON c.id_materia = m.id_materia
            LEFT JOIN usuarios u ON c.id_profesor = u.id_usuario
            WHERE c.id_curso = %s
        """
        result = query_db(sql, (id_course,))

        if not result:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No existe un curso con ID {id_course}"
            }

        course = result[0]

        ayudantes = query_db("""
            SELECT u.id_usuario, u.nombre, u.apellido
            FROM curso_ayudantes ca
            JOIN usuarios u ON ca.id_usuario = u.id_usuario
            WHERE ca.id_curso = %s
        """, (id_course,))

        course["ayudantes"] = ayudantes

        return {
            "ok": True,
            "data": course
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }

def create_course(data):
    try:
        id_materia = data.get('id_materia')
        catedra = data.get('catedra')
        term = data.get('cuatrimestre')
        year = data.get('anio')
        id_profe = data.get('id_profesor')

        sql = """
            INSERT INTO cursos (id_materia, catedra, cuatrimestre, anio, id_profesor)
            VALUES (%s, %s, %s, %s, %s)
        """
        modify_db(sql, (id_materia, catedra, term, int(year), id_profe))
        return {
            "ok": True,
            "message": "curso creado correctamente"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": str(e)
        }

def patch_course(id_course, data):
    try:
        id_materia = data.get('id_materia')
        catedra = data.get('catedra')
        term = data.get('cuatrimestre')
        year = data.get('anio')
        id_profe = data.get('id_profesor')
        slack_url   = data.get('slack_url')
        youtube_url = data.get('youtube_url')
        regimen_aprobacion = data.get('regimen_aprobacion')
        updates = []
        params = []

        if id_materia is not None:
            updates.append("id_materia = %s")
            params.append(id_materia)
        if catedra is not None:
            updates.append("catedra = %s")
            params.append(catedra)
        if term is not None:
            updates.append("cuatrimestre = %s")
            params.append(term)
        if year is not None:
            updates.append("anio = %s")
            params.append(int(year))
        if id_profe is not None:
            updates.append("id_profesor = %s")
            params.append(id_profe)
        if slack_url is not None:
            updates.append("slack_url = %s")
            params.append(slack_url if slack_url.strip() else None)
        if youtube_url is not None:
            updates.append("youtube_url = %s")
            params.append(youtube_url if youtube_url.strip() else None )
        if regimen_aprobacion is not None:
            updates.append("regimen_aprobacion = %s")
            params.append(regimen_aprobacion)

        if not updates:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "No se enviaron campos para actualizar"
            }

        sql = f"UPDATE cursos SET {', '.join(updates)} WHERE id_curso = %s"
        params.append(id_course)

        exists = query_db("SELECT id_curso FROM cursos WHERE id_curso = %s", (id_course,))
        if not exists:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No hay un curso con el id {id_course} para actualizar"
            }
        modify_db(sql, params)
        
        return {
            "ok": True,
            "message": "Curso actualizado con éxito",
            "id_curso": id_course
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": str(e)
        }

def delete_course(id_course):
    try:
        sql = "DELETE FROM cursos WHERE id_curso = %s"
        modify_row = modify_db(sql, (id_course,))

        if modify_row == 0:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No se encontró el curso con el ID {id_course}."
            }
        return {
            "ok": True,
            "message": f"Curso con ID {id_course} eliminado correctamente"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }
    

def get_assistants_by_course(id_curso):
    try:
        query = """
            SELECT 
                u.id_usuario,
                u.nombre,
                u.apellido,
                u.correo
            FROM curso_ayudantes ca
            JOIN usuarios u ON u.id_usuario = ca.id_usuario
            WHERE ca.id_curso = %s
        """

        assistants = query_db(query, (id_curso,))

        return {
            "ok": True,
            "data": assistants
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }
    
def assign_assistant_to_course(id_curso, id_ayudante, id_user, id_rol):
    try:
        course = query_db(
            """
            SELECT id_curso, id_profesor
            FROM cursos
            WHERE id_curso = %s
            """,
            (id_curso,)
        )

        if not course:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": "El curso no existe"
            }

        course = course[0]

        id_rol = int(id_rol)
        id_user = int(id_user)
        id_profesor = int(course["id_profesor"])

        es_superadmin = id_rol == 1
        es_profesor_del_curso = id_rol == 2 and id_user == id_profesor

        if not es_superadmin and not es_profesor_del_curso:
            return {
                "ok": False,
                "code": 403,
                "message": "Forbidden",
                "description": "No tenés permiso para asignar ayudantes a este curso"
            }

        assistant = query_db(
            """
            SELECT id_usuario
            FROM usuarios
            WHERE id_usuario = %s
            AND id_rol = 3
            """,
            (id_ayudante,)
        )

        if not assistant:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "El usuario seleccionado no existe o no tiene rol de ayudante"
            }

        query = """
            INSERT IGNORE INTO curso_ayudantes (id_curso, id_usuario)
            VALUES (%s, %s)
        """

        modify_db(query, (id_curso, id_ayudante))

        return {
            "ok": True,
            "message": "Ayudante asignado al curso correctamente"
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }
    
def remove_assistant_from_course(id_curso, id_ayudante, user):
    try:
        id_user = int(user["id_usuario"])
        id_rol = int(user["id_rol"])
        course = query_db(
            """
            SELECT id_curso, id_profesor
            FROM cursos
            WHERE id_curso = %s
            """,
            (id_curso,)
        )

        if not course:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": "El curso no existe"
            }

        course = course[0]

        id_user = int(id_user)
        id_rol = int(id_rol)
        id_profesor = int(course["id_profesor"])

        es_superadmin = id_rol == 1
        es_profesor_del_curso = id_rol == 2 and id_user == id_profesor

        if not es_superadmin and not es_profesor_del_curso:
            return {
                "ok": False,
                "code": 403,
                "message": "Forbidden",
                "description": "No tenés permiso para quitar ayudantes de este curso"
            }

        query = """
            DELETE FROM curso_ayudantes
            WHERE id_curso = %s
            AND id_usuario = %s
        """

        modify_db(query, (id_curso, id_ayudante))

        return {
            "ok": True,
            "message": "Ayudante quitado del curso correctamente"
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }
