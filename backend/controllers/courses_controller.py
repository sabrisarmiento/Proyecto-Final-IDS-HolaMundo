from database.db import query_db, modify_db

def get_all_courses(filters):
    try:
        name = filters.get('nombre')
        term = filters.get('cuatrimestre')
        year = filters.get('anio')

        sql = "SELECT id_curso, nombre, cuatrimestre, anio FROM cursos"
        condition = " WHERE 1=1"
        params = []

        if name is not None:
            condition += " AND nombre LIKE %s"
            params.append(f"%{name}%")

        if term is not None:
            condition += " AND cuatrimestre = %s"
            params.append(term)

        if year is not None:
            condition += " AND anio = %s"
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
        sql = "SELECT id_curso, nombre, cuatrimestre, anio FROM cursos WHERE id_curso = %s"
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
            "data": result
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
        name = data.get('nombre')
        term = data.get('cuatrimestre')
        year = data.get('anio')

        sql = """
            INSERT INTO cursos (nombre, cuatrimestre, anio)
            VALUES (%s, %s, %s)
        """
        modify_db(sql, (name, term, int(year)))
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
        name = data.get('nombre')
        term = data.get('cuatrimestre')
        year = data.get('anio')

        updates = []
        params = []

        if name is not None:
            updates.append("nombre = %s")
            params.append(name)
        if term is not None:
            updates.append("cuatrimestre = %s")
            params.append(term)
        if year is not None:
            updates.append("anio = %s")
            params.append(int(year))

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