from database.db import query_db, modify_db

def get_all_exam_types():
    return query_db("SELECT * FROM tipos_evaluacion")

def get_exam_type_by_id(id):
    result = query_db("SELECT * FROM tipos_evaluacion WHERE id_tipo = %s", (id,))
    return result[0] if result else None

def create_exam_type(data):
    query = "INSERT INTO tipos_evaluacion (nombre, descripcion) VALUES (%s, %s)"
    return modify_db(query, (data["nombre"], data.get("descripcion")))

def update_exam_type(id, data):
    fields = []
    values = []

    if "nombre" in data:
        fields.append("nombre = %s")
        values.append(data["nombre"])
    if "descripcion" in data:
        fields.append("descripcion = %s")
        values.append(data["descripcion"])

    if not fields:
        return False

    values.append(id)
    modify_db(f"UPDATE tipos_evaluacion SET {', '.join(fields)} WHERE id_tipo = %s", values)
    return True

def delete_exam_type(id):
    result = query_db("SELECT id_tipo FROM tipos_evaluacion WHERE id_tipo = %s", (id,))
    if not result:
        return False
    modify_db("DELETE FROM tipos_evaluacion WHERE id_tipo = %s", (id,))
    return True
