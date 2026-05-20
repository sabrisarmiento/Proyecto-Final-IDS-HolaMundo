from database.db import query_db, modify_db 

def get_classes(date_param=None):
    if date_param:
        query = "SELECT * FROM CLASES WHERE fecha = %s"
        return query_db(query, (date_param,))
    else:
        query = "SELECT * FROM CLASES"
        return query_db(query)

def get_class_id(class_id):
    query = "SELECT * FROM CLASES WHERE id_clase = %s"
    result = query_db(query, (class_id,))
    return result if result else None

def create_class(data):
    query = "INSERT INTO CLASES (fecha, temas, id_curso) VALUES (%s, %s, %s)"
    values = (data['date'], data.get('topics', ''), data['course_id'])
    return modify_db(query, values)

def update_class(class_id, data):
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
        
    if not fields:
        return False
        
    values.append(class_id)
    query = f"UPDATE CLASES SET {', '.join(fields)} WHERE id_clase = %s"
    
    modify_db(query, values)
    return True