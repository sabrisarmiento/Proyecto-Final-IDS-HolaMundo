from database.db import query_db, modify_db

def get_all_subjects(filters):
  try:
    name=filters.get("name")

    sql = "SELECT id_materia, nombre, codigo FROM materias"
    condition = " WHERE 1=1"
    params = []
    if name is not None:
      condition += " AND nombre = %s"
      params.append(name)
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

def get_subject_by_id(id):
  try:
    if id <= 0:
      return {
        "ok": False,
        "code": 400,
        "message": "Bad Request",
        "description": "El ID debe ser un número entero positivo"
      }

    result = query_db("SELECT * FROM materias WHERE id_materia = %s", (id,))
    if not result:
      return {
        "ok": False,
        "code": 404,
        "message": "Not Found",
        "description": f"No existe una materia con ID {id}"
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

def create_subject(data):
  try:
    if not data:
      return {
        "ok": False,
        "code": 400,
        "message": "Bad Request",
        "description": "Los datos de la materia son requeridos"
      }

    if not data.get("nombre"):
      return {
        "ok": False,
        "code": 400,
        "message": "Bad Request",
        "description": "El nombre de la materia es requerido"
      }

    codigo = data.get("codigo") or None

    if codigo:
      exists = query_db("SELECT id_materia FROM materias WHERE codigo = %s", (codigo,))
      if exists:
        return {
          "ok": False,
          "code": 409,
          "message": "Conflict",
          "description": f"Ya existe una materia con el código {codigo}"
        }

    sql = "INSERT INTO materias (nombre, codigo) VALUES (%s, %s)"
    modify_db(sql, (data["nombre"], codigo))
    return {
      "ok": True,
      "message": "Materia creada exitosamente"
    }
  except Exception as e:
    return {
      "ok": False,
      "code": 500,
      "message": "Internal Server Error",
      "description": str(e)
    }

def patch_subject(id, data):
  try:
    if id <= 0:
      return {
        "ok": False,
        "code": 400,
        "message": "Bad Request",
        "description": "El ID debe ser un número entero positivo"
      }

    exists = query_db("SELECT id_materia FROM materias WHERE id_materia = %s", (id,))
    if not exists:
      return {
        "ok": False,
        "code": 404,
        "message": "Not Found",
        "description": f"No existe una materia con ID {id}"
      }

    updates = []
    params = []

    if data.get("nombre"):
      updates.append("nombre = %s")
      params.append(data["nombre"])

    if data.get("codigo"):
      codigo_exists = query_db(
        "SELECT id_materia FROM materias WHERE codigo = %s AND id_materia != %s",
        (data["codigo"], id)
      )
      if codigo_exists:
        return {
          "ok": False,
          "code": 409,
          "message": "Conflict",
          "description": f"Ya existe otra materia con el código {data['codigo']}"
        }
      updates.append("codigo = %s")
      params.append(data["codigo"])

    if not updates:
      return {
        "ok": False,
        "code": 400,
        "message": "Bad Request",
        "description": "No se enviaron campos para actualizar"
      }

    params.append(id)
    sql = f"UPDATE materias SET {', '.join(updates)} WHERE id_materia = %s"
    modify_db(sql, params)
    return {
      "ok": True,
      "message": "Materia actualizada correctamente"
    }
  except Exception as e:
    return {
      "ok": False,
      "code": 500,
      "message": "Internal Server Error",
      "description": str(e)
    }

def delete_subject(id):
  try:
    if id <= 0:
      return {
        "ok": False,
        "code": 400,
        "message": "Bad Request",
        "description": "El ID debe ser un número entero positivo"
      }

    exists = query_db("SELECT id_materia FROM materias WHERE id_materia = %s", (id,))
    if not exists:
      return {
        "ok": False,
        "code": 404,
        "message": "Not Found",
        "description": f"No existe una materia con ID {id}"
      }

    cursos_asociados = query_db(
      "SELECT id_curso FROM cursos WHERE id_materia = %s LIMIT 1", (id,)
    )
    if cursos_asociados:
      return {
        "ok": False,
        "code": 409,
        "message": "Conflict",
        "description": "No se puede eliminar la materia porque tiene cursos asociados"
      }

    modify_db("DELETE FROM materias WHERE id_materia = %s", (id,))
    return {
      "ok": True,
      "message": f"Materia con ID {id} eliminada correctamente"
    }
  except Exception as e:
    return {
      "ok": False,
      "code": 500,
      "message": "Internal Server Error",
      "description": str(e)
    }