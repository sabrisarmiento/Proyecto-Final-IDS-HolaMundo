from database.db import query_db, modify_db

def get_all_courses(filters):
    try:
        materia = filters.get('materia')
        catedra = filters.get('catedra')
        year = filters.get('anio')

        sql = """
            SELECT c.id_curso, m.nombre AS materia, c.catedra, c.cuatrimestre, c.anio 
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

def get_course_id(id_course):
    try:
        sql = """
            SELECT c.id_curso, m.nombre AS materia, c.catedra, c.cuatrimestre, c.anio 
            FROM cursos c
            JOIN materias m ON c.id_materia = m.id_materia
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

        if not updates:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "No se enviaron campos para actualizar"
            }

        sql = f"UPDATE cursos SET {', '.join(updates)} WHERE id_curso = %s"
        params.append(id_course)

        modify_row = modify_db(sql, params)
        if modify_row == 0:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No hay un curso con el id {id_course} para actualizar"
            }
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