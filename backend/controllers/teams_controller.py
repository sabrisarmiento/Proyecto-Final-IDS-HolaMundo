from database.db import query_db, modify_db

def get_all_teams(filters):
    try:
        id_student = filters.get("id_alumno")
        id_course = filters.get("id_curso")
        sql = """
        SELECT
            e.id_equipo,
            e.nombre_equipo,
            e.id_curso,
            a.id_alumno,
            a.nombre,
            a.apellido,
            a.padron
        FROM equipos e
        LEFT JOIN equipo_alumno ea
            ON e.id_equipo = ea.id_equipo
        LEFT JOIN alumnos a
            ON ea.id_alumno = a.id_alumno
        """
        condition = " WHERE 1=1 "
        params = []
        if id_student is not None:
            condition += " AND e.id_equipo IN (SELECT id_equipo FROM equipo_alumno WHERE id_alumno = %s) "
            params.append(int(id_student))
        if id_course is not None:
            condition += " AND e.id_curso = %s"
            params.append(int(id_course))
        result = query_db(sql + condition, params)
        equipos = {}
        for row in result:
            id_equipo = row["id_equipo"]
            if id_equipo not in equipos:
                equipos[id_equipo] = {
                    "id_equipo": row["id_equipo"],
                    "nombre_equipo": row["nombre_equipo"],
                    "id_curso": row["id_curso"],
                    "alumnos": []
                }
            if row["id_alumno"] is not None:
                equipos[id_equipo]["alumnos"].append({
                    "id_alumno": row["id_alumno"],
                    "nombre": row["nombre"],
                    "apellido": row["apellido"],
                    "padron": row["padron"]
                })
        return {
            "ok": True,
            "data": list(equipos.values())
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }

def get_team_by_id(id):
    try:
        sql = """
        SELECT
            e.id_equipo,
            e.nombre_equipo,
            e.id_curso,
            a.id_alumno,
            a.nombre,
            a.apellido,
            a.padron
        FROM equipos e
        LEFT JOIN equipo_alumno ea ON e.id_equipo = ea.id_equipo
        LEFT JOIN alumnos a ON ea.id_alumno = a.id_alumno
        WHERE e.id_equipo = %s
        """
        result = query_db(sql, (id,))
        if not result:
            return {
                "ok": False,
                "code": 404,
                "message": "Team not found",
                "description": f"No existe un equipo con id {id}"
            }
        equipo = {
            "id_equipo": result[0]["id_equipo"],
            "nombre_equipo": result[0]["nombre_equipo"],
            "id_curso": result[0]["id_curso"],
            "alumnos": []
        }
        for row in result:
            if row["id_alumno"] is not None:
                equipo["alumnos"].append({
                    "id_alumno": row["id_alumno"],
                    "nombre": row["nombre"],
                    "apellido": row["apellido"],
                    "padron": row["padron"]
                })
        return {
            "ok": True,
            "data": equipo
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }

def create_team(data):
    try:
        name = data.get("nombre_equipo")
        id_course = data.get("id_curso")
        sql = """INSERT INTO equipos(nombre_equipo, id_curso) VALUES (%s, %s);"""
        id_team = modify_db(sql, (name, id_course))
        return {
            "ok": True,
            "message": "Equipo creado correctamente",
            "id_equipo": id_team,
            "nombre_equipo": name,
            "id_curso": id_course
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }

def patch_team_by_id(id_team, data):
    try:
        name = data.get('nombre_equipo')
        id_course = data.get('id_curso')
        updates = []
        params = []
        if name is not None:
            updates.append("nombre_equipo = %s")
            params.append(name)
        if id_course is not None:
            updates.append("id_curso = %s")
            params.append(int(id_course))
        if not updates:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "No se enviaron campos para actualizar"
            }
        sql = f"""UPDATE equipos SET {', '.join(updates)} WHERE id_equipo = %s"""
        params.append(id_team)
        modify_db(sql, params)
        return {
            "ok": True,
            "message": "Equipo actualizado correctamente"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": str(e)
        }

def delete_team_by_id(id_team):
    try:
        sql = """DELETE FROM equipos WHERE id_equipo = %s"""
        modify_db(sql, (id_team,))
        return {
            "ok": True,
            "message": f"Equipo con ID {id_team} eliminado correctamente"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }
