from database.db import query_db, modify_db

def get_all_exams(filters):
    try:
        id_type=filters.get('id_tipo')
        id_user=filters.get('id_usuario')
        date=filters.get('fecha')

        sql = "SELECT id_tipo, id_user, fecha FROM evaluaciones"
        condition= "WHERE 1=1"
        params = []

        if id_type is not None:
            condition+="AND id_type=%s"
            params.append(int(id_type))

        if id_user is not None:
            condition*="AND id_user=%s"
            params.append(int(id_user))
        
        if date is not None:
            condition+="AND date=%s"
            params.append(int(date))
        
        result=query_db(sql + condition, params)
        return {
            "ok":True,
            "data":result
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }
    

#-----------------------------------------------------------


def get_exam_by_id(id_exam):
    try:
        sql="SELECT id_tipo, id_user, fecha FROM evaluaciones"
        result=query_db(sql,(id_exam,))

        if not result:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No existe una evaluación con ID {id_exam}"
            }
        return {
            "ok": True,
            "data":result
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }


#-----------------------------------------------------------


def create_exam(data):
    try:

        id_type=data.get('id_tipo')
        id_user=data.get('id_usuario')
        date=data.get('fecha')

        sql = """
            INSERT INTO evaluaciones (id_type, id_user, date)
            VALUES (%s, %s, %s, %s, %s)
        """
        modify_db(sql, (id_type, id_user, date))
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


#-----------------------------------------------------------

def patch_exam_by_id(id_exam,data):
    try:   
        id_type=data.get('id_tipo')
        id_user=data.get('id_usuario')
        date=data.get('fecha')
            
        updates = []
        params = []

        if id_type is not None:
            updates.append("id_alumno = %s")
            params.append(int(id_type))
        if id_user is not None:
            updates.append("id_evaluacion = %s")
            params.append(int(id_user))
        if date is not None:
            updates.append("id_equipo = %s")
            params.append(int(date))

        if not updates:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "No se enviaron campos para actualizar"
            }

        sql = f"UPDATE evaluaciones SET {', '.join(updates)} WHERE id_evaluacion = %s"
        params.append(id_exam)
    
        modify_row = modify_db(sql, params)
        if modify_row == 0:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No hay una evaluacion con el id {id_exam} para actualizar"
            }
        return {
            "ok": True,
            "message": "Evaluacion actualizada con éxito",
            "id_evaluacion": id_exam
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": str(e)
        }

#-----------------------------------------------------------

def delete_exam_by_id(id_exam):
    try:    
        sql = "DELETE FROM evaluaciones WHERE id_evaluacion= %s"

        modify_row = modify_db(sql, (id_exam,))

        if modify_row == 0:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No se encontró la evaluacion con el ID {id_exam}."
            }
        return {
            "ok": True,
            "message": f"Evaluacion con ID {id_exam} eliminada correctamente"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }
