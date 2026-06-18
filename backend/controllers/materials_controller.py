from database.db import query_db, modify_db

def get_all_materials(filters):
    try:
        id_course = filters.get('id_curso')
        title = filters.get('titulo')

        if id_course:
            if not str(id_course).isdigit():
                return {"ok": False, "code": 400, "message": "Bad Request",
                        "description": "id_curso debe ser un entero"}
            id_course = int(id_course)
        else:
            id_course = None

        sql = """
            SELECT m.id_material, m.titulo, m.descripcion, m.url_externo, m.id_curso,
            m.id_clase, c.temas AS clase_temas, c.fecha AS clase_fecha
            FROM materiales m
            LEFT JOIN clases c ON m.id_clase = c.id_clase
        """
        condition = " WHERE 1=1"
        params = []

        if id_course is not None:
            condition += " AND m.id_curso = %s"
            params.append(id_course)

        if title:
            condition += " AND m.titulo LIKE %s"
            params.append(f"%{title}%")

        result = query_db(sql + condition, params)
        return {"ok": True, "data": result}
    except Exception as e:
        return {"ok": False, "code": 500, "message": "Internal Server Error",
                "description": str(e)}
    
def create_material(data):
    try:
        title = data.get('titulo')
        description = data.get('descripcion')
        url = data.get('url_externo')
        id_course = data.get('id_curso')
        id_class = data.get('id_clase') or None

        sql = "INSERT INTO materiales (titulo, descripcion, url_externo, id_curso, id_clase) VALUES (%s, %s, %s, %s, %s)"

        modify_db(sql, (title, description, url, id_course, id_class))

        return {
            "ok": True,
            "message": "Material creado."
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": str(e)
        }
    
def delete_material_by_id(id_material):
    try:
        sql = "DELETE FROM materiales WHERE id_material = %s"
        modify_row = modify_db(sql, (id_material,))
        if modify_row == 0:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": f"No se encontró el material con el ID {id_material}."
            }
        return {
            "ok": True,
            "message": f"Material con ID {id_material} eliminado correctamente"
        }
    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }
    
def update_material(id_material, data):
    try:
        exists = query_db("SELECT id_material FROM materiales WHERE id_material = %s", (id_material,))
        if not exists:
            return {"ok": False, "code": 404, "message": "Not Found",
                    "description": f"No existe el material con el ID {id_material}."}

        fields, params = [], []
        for key in ["titulo", "descripcion", "url_externo"]:
            if key in data and data[key] is not None:
                fields.append(f"{key} = %s")
                params.append(data[key])

        if "id_clase" in data:
            fields.append("id_clase = %s")
            params.append(data["id_clase"] or None)

        if not fields:
            return {"ok": False, "code": 400, "message": "Bad Request",
                    "description": "No se enviaron campos para actualizar"}

        params.append(id_material)
        modify_db(f"UPDATE materiales SET {', '.join(fields)} WHERE id_material = %s", tuple(params))
        return {"ok": True, "message": "Material actualizado correctamente"}
    except Exception as e:
        return {"ok": False, "code": 500, "message": "Internal Server Error",
                "description": str(e)}
