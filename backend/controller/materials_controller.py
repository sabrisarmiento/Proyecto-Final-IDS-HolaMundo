from database.db import query_db, modify_db

def get_all_materials(filters):
    try:
        id_course = filters.get('id_curso')
        title = filters.get('titulo')

        sql = "SELECT id_material, titulo, descripcion, url_externo, id_curso FROM materiales"

        condition = " WHERE 1=1"
        params = []

        if id_course is not None:
            condition += " AND id_curso = %s"
            params.append(int(id_course))
        
        if title is not None:
            condition += " AND titulo = %s"
            params.append(title)

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
    
def create_material(data):
    try:
        title = data.get('titulo')
        description = data.get('descripcion')
        url = data.get('url_externo')
        id_course = data.get('id_curso')

        sql = "INSERT INTO materiales (titulo, descripcion, url_externo, id_curso) VALUES (%s, %s, %s, %s)"

        modify_db(sql, (title, description, url, id_course))

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