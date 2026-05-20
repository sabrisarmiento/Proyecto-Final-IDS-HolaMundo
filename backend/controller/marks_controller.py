from database.db import query_db, modify_db

def get_all_marks(filters):
    try:
        id_student = filters.get('id_alumno')
        id_evaluation = filters.get('id_evaluacion')
        id_team = filters.get('id_equipo')
        id_grader = filters.get('id_corrector')
        mark_filter = filters.get('nota')

        sql = "SELECT id_nota, id_alumno, id_evaluacion, nota FROM notas"
        condition = " WHERE 1=1" 
        params = []

        if id_student is not None:
            condition += " AND id_alumno = %s"
            params.append(int(id_student))

        if id_evaluation is not None:
            condition += " AND id_evaluacion = %s"
            params.append(int(id_evaluation))
        
        if id_team is not None:
            condition += " AND id_equipo = %s"
            params.append(int(id_team))

        if id_grader is not None:
            condition += " AND id_corrector = %s"
            params.append(int(id_grader))

        if mark_filter is not None:
            condition += " AND nota = %s"
            params.append(float(mark_filter))

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

def get_mark_by_id(id_mark):
    try:
        sql = "SELECT id_nota, id_alumno, id_evaluacion, nota FROM notas WHERE id_nota = %s"

        result = query_db(sql, (id_mark,))

        if not result:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No existe una nota con ID {id_mark}"
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


def create_mark(data):
    try:

        id_team = data.get('id_equipo')
        id_student = data.get('id_alumno')
        id_evaluation = data.get('id_evaluacion')
        id_grader = data.get('id_corrector')
        mark_value = data.get('nota')

        sql = """
            INSERT INTO notas (id_alumno, id_evaluacion, nota, id_equipo, id_corrector)
            VALUES (%s, %s, %s, %s, %s)
        """
        modify_db(sql, (id_student, id_evaluation, float(mark_value), id_team, id_grader))
        return {
            "ok": True
            }
    except Exception as e:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": str(e)
        }
    
def patch_mark_by_id(id_mark, data):
    try:
            
        id_student = data.get('id_alumno')
        id_evaluation = data.get('id_evaluacion')
        id_team = data.get('id_equipo')
        mark_value = data.get('nota')
        id_grader = data.get('id_corrector') 
            
        updates = []
        params = []

        if id_student is not None:
            updates.append("id_alumno = %s")
            params.append(int(id_student))
        if id_evaluation is not None:
            updates.append("id_evaluacion = %s")
            params.append(int(id_evaluation))
        if id_team is not None:
            updates.append("id_equipo = %s")
            params.append(int(id_team))
        if mark_value is not None:
            updates.append("nota = %s")
            params.append(float(mark_value))
        if id_grader is not None:
            updates.append("id_corrector = %s")
            params.append(int(id_grader))

        if not updates:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "No se enviaron campos para actualizar"
            }

        sql = f"UPDATE notas SET {', '.join(updates)} WHERE id_nota = %s"
        params.append(id_mark)
    
        modify_row = modify_db(sql, params)
        if modify_row == 0:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No hay una nota con el id {id_mark} para actualizar"
            }
        return {
            "ok": True,
            "message": "Nota actualizada con éxito",
            "id_nota": id_mark
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": str(e)
        }
    

def delete_mark_by_id(id_mark):
    try:    
        sql = "DELETE FROM notas WHERE id_nota = %s"

        modify_row = modify_db(sql, (id_mark,))

        if modify_row == 0:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No se encontró la nota con el ID {id_mark}."
            }
        return {
            "ok": True,
            "message": f"Nota con ID {id_mark} eliminada correctamente"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }
