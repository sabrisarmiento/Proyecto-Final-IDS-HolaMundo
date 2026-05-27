from database.db import query_db, modify_db 

def get_classes(filters):
    try:
        fecha = filters.get('fecha')
        
        id_curso = filters.get('id_curso')
        if id_curso is None or id_curso == '':
            id_curso = 1
        
        query = "SELECT id_clase, fecha, temas, tipo, modalidad, semana, id_curso FROM clases"
        condition = " WHERE 1=1"
        params = []
        
        if fecha:
            condition += " AND fecha = %s"
            params.append(fecha)
        
        condition += " AND id_curso = %s"
        params.append(int(id_curso))
        

        final_query = query + condition + " ORDER BY semana ASC, fecha ASC"
        
        result = query_db(final_query, params)

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
        query = "SELECT id_clase, fecha, temas, tipo, modalidad, semana, id_curso FROM clases WHERE id_clase = %s"
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
            "data": result[0]
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
        fecha = data.get('fecha')
        temas = data.get('temas', '')
        semana = data.get('semana')
        tipo = data.get('tipo')
        modalidad = data.get('modalidad')
        id_curso = data.get('id_curso')

        if not fecha or not id_curso or not semana:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "Faltan campos obligatorios: fecha, semana e id_curso"
            }
        
        query = """
            INSERT INTO clases (fecha, temas, semana, tipo, modalidad, id_curso) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        modify_db(query, (fecha, temas, semana, tipo, modalidad, id_curso))

        return {
            "ok": True,
            "message": "Clase creada correctamente"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }

def update_class(id_clase, data):
    try:
        fields = []
        values = []
        
        allowed_fields = ['fecha', 'temas', 'semana', 'tipo', 'modalidad', 'id_curso']
        
        for field in allowed_fields:
            if field in data:
                fields.append(f"{field} = %s")
                values.append(data[field])
        
        if not fields:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "No se enviaron campos para actualizar"
            }
        
        values.append(id_clase)
        query = f"UPDATE clases SET {', '.join(fields)} WHERE id_clase = %s"
        
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

def delete_class(id_clase):
    try:
        query = "DELETE FROM clases WHERE id_clase = %s"
        affected_rows = modify_db(query, (id_clase,))
        
        if affected_rows == 0:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No se encontró la clase con el ID {id_clase}"
            }
        
        return {
            "ok": True,
            "message": f"Clase con ID {id_clase} eliminada correctamente"
        }
    
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }