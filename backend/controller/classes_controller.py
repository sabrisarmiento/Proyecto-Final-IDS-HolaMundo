from database.db import query_db, modify_db 

def get_classes(filters):
    try:
        fecha = filters.get('fecha')
        query = "SELECT * FROM CLASES WHERE fecha = %s"
        condition = "WHERE 1=1"
        params = []
        if fecha is not None:
            condition += "AND fecha = %s"
            params.append(fecha)
        
        result = query_db(query + condition, params)

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

def get_class_id(id_clase):
    try:
        query = "SELECT id_clase, fecha, temas, id_curso FROM CLASES WHERE id_clase = %s"
        result = query_db(query, (id_clase,))

        if not result:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No se encontró la clase con el ID {id_clase}"
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

def create_class(data):
    try:
        date = data.get('fecha')
        topics = data.get('temas', '')
        course_id = data.get('id_curso')

        if not date or not course_id:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "Faltan campos obligatorios: fecha e id_curso"
            }
        
        query = "INSERT INTO CLASES (fecha, temas, id_curso) VALUES (%s, %s, %s)"
        modify_db(query, (date, topics, course_id))

        return {
                "ok": True,
                "description": "Clase creada correctamente"
            }
    except Exception as e:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": str(e)
        }

def update_class(id_clase, data):
    try:
        fields = []
        values = []
    
        if 'date' in data:
            fields.append("fecha = %s")
            values.append(data['date'])
        if 'topics' in data:
            fields.append("temas = %s")
            values.append(data['topics'])
        if 'course_id' in data:
            fields.append("id_curso = %s")
            values.append(data['course_id'])
        
        if len(fields) == 0:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "No se enviaron campos para actualizar"
            }
        
        values.append(id_clase)
        query = f"UPDATE CLASES SET {', '.join(fields)} WHERE id_clase = %s"
    
        modify_db(query, values)

        return {
            "ok": True,
            "message": f"Clase con ID {id_clase} actualizada correctamente"
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }