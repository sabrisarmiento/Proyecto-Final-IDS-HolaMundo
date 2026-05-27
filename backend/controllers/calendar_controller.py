from database.db import query_db, modify_db

def get_all_events(filters):
    try:
        id_profesor = filters.get('id_profesor')
        fecha = filters.get('fecha_evento')
        tipo = filters.get('tipo_clase')

        sql = "SELECT id_evento, titulo, tipo_clase, descripcion, modalidad, hipervinculo, fecha_evento, id_profesor FROM calendario"
        condition = " WHERE 1=1" 
        params = []

        if id_profesor is not None:
            condition += " AND id_profesor = %s"
            params.append(int(id_profesor))

        if fecha is not None:
            condition += " AND DATE(fecha_evento) = %s"
            params.append(fecha)
            
        if tipo is not None:
            condition += " AND tipo_clase = %s"
            params.append(tipo)

        result = query_db(sql + condition, params)
        return {"ok": True, "data": result}
    except Exception as e:
        return {"ok": False, "code": 500, "message": "Error Interno", "description": str(e)}

def get_event_by_id(id_event):
    try:
        sql = "SELECT * FROM calendario WHERE id_evento = %s"
        result = query_db(sql, (id_event,))
        if not result:
            return {"ok": False, "code": 404, "message": "No encontrado", "description": f"ID {id_event} no existe"}
        return {"ok": True, "data": result}
    except Exception as e:
        return {"ok": False, "code": 500, "description": str(e)}

def create_event(data):
    try:
        sql = """
            INSERT INTO calendario (titulo, tipo_clase, descripcion, modalidad, hipervinculo, fecha_evento, id_profesor)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data.get('titulo'), data.get('tipo_clase'), data.get('descripcion'),
            data.get('modalidad'), data.get('hipervinculo'), data.get('fecha_evento'),
            data.get('id_profesor')
        )
        modify_db(sql, params)
        return {"ok": True, "message": "Evento de calendario creado con éxito"}
    except Exception as e:
        return {"ok": False, "code": 400, "description": str(e)}

def patch_event_by_id(id_event, data):
    try:
        fields = ['titulo', 'tipo_clase', 'descripcion', 'modalidad', 'hipervinculo', 'fecha_evento', 'id_profesor']
        updates = []
        params = []

        for field in fields:
            if field in data:
                updates.append(f"{field} = %s")
                params.append(data.get(field))

        if not updates:
            return {"ok": False, "code": 400, "message": "Nada que actualizar"}

        sql = f"UPDATE calendario SET {', '.join(updates)} WHERE id_evento = %s"
        params.append(id_event)
        
        if modify_db(sql, params) == 0:
            return {"ok": False, "code": 404, "message": "Evento no encontrado"}
        return {"ok": True, "message": "Evento actualizado", "id_evento": id_event}
    except Exception as e:
        return {"ok": False, "code": 400, "description": str(e)}

def delete_event_by_id(id_event):
    try:
        sql = "DELETE FROM calendario WHERE id_evento = %s"
        if modify_db(sql, (id_event,)) == 0:
            return {"ok": False, "code": 404, "message": "Evento no encontrado"}
        return {"ok": True, "message": "Evento eliminado correctamente"}
    except Exception as e:
        return {"ok": False, "code": 500, "description": str(e)}