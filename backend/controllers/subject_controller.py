from database.db import query_db, modify_db, insert_db

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

def get_subjects_for_user(id_user, is_admin, filters):
    try:
        if is_admin:
            return get_all_subjects(filters)

        sql = "SELECT id_materia, nombre, codigo FROM materias"
        condition = """
            WHERE id_materia IN (
                SELECT id_materia FROM materia_profesores WHERE id_usuario = %s
                UNION
                SELECT DISTINCT id_materia FROM cursos
                WHERE id_profesor = %s
                OR id_curso IN (SELECT id_curso FROM curso_ayudantes WHERE id_usuario = %s)
            )
        """
        params = [id_user, id_user, id_user]
        if filters.get("name"):
            condition += " AND nombre = %s"; params.append(filters["name"])

        return {"ok": True, "data": query_db(sql + condition, params)}
    except Exception as e:
        return {"ok": False, "code": 500, "message": "Internal Server Error", "description": str(e)}


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

def get_topics_by_subject_id(id):
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

        result = query_db(
            "SELECT id_tema, nombre, icono, orden FROM materia_temas WHERE id_materia = %s ORDER BY orden ASC",
            (id,)
        )
        return {"ok": True, "data": result}
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
    ids_profesores = data.get("ids_profesores", [])

    if data.get("id_profesor"):
      ids_profesores.append(data.get("id_profesor"))

    if codigo:
      exists = query_db("SELECT id_materia FROM materias WHERE codigo = %s", (codigo,))
      if exists:
        return {
          "ok": False,
          "code": 409,
          "message": "Conflict",
          "description": f"Ya existe una materia con el código {codigo}"
        }
      
    for id_profesor in ids_profesores:
      profesor = query_db(
        "SELECT id_usuario FROM usuarios WHERE id_usuario = %s AND id_rol = 2",
        (id_profesor,)
      )

      if not profesor:
        return {
          "ok": False,
          "code": 400,
          "message": "Bad Request",
          "description": "El profesor con id {id_profesor} no existe o no tiene rol de profesor"
        }
    sql = "INSERT INTO materias (nombre, codigo) VALUES (%s, %s)"
    id_materia = insert_db(sql, (data["nombre"], codigo))

    for id_profesor in ids_profesores:
      sql_asignacion = """
        INSERT IGNORE INTO materia_profesores (id_materia, id_usuario)
        VALUES (%s, %s)
      """

      modify_db(sql_asignacion, (id_materia, id_profesor))

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
  
def get_professors_by_subject(id_materia):
  try:
    query = """
      SELECT
        u.id_usuario,
        u.nombre,
        u.apellido,
        u.correo
      FROM materia_profesores mp
      JOIN usuarios u ON u.id_usuario = mp.id_usuario
      WHERE mp.id_materia = %s
    """

    professors = query_db(query, (id_materia,))

    return {
      "ok": True,
      "data": professors
    }

  except Exception as e:
    return {
      "ok": False,
      "code": 500,
      "message": "Internal Server Error",
      "description": str(e)
    }
  

def assign_professor_to_subject(id_materia, id_profesor):
  try:
    subject = query_db(
      "SELECT id_materia FROM materias WHERE id_materia = %s",
      (id_materia,)
    )

    if not subject:
      return {
        "ok": False,
        "code": 404,
        "message": "Not Found",
        "description": "La materia no existe"
      }

    professor = query_db(
      "SELECT id_usuario FROM usuarios WHERE id_usuario = %s AND id_rol = 2",
      (id_profesor,)
    )

    if not professor:
      return {
        "ok": False,
        "code": 400,
        "message": "Bad Request",
        "description": "El usuario seleccionado no existe o no tiene rol de profesor"
      }

    sql = """
      INSERT IGNORE INTO materia_profesores (id_materia, id_usuario)
      VALUES (%s, %s)
    """

    modify_db(sql, (id_materia, id_profesor))

    return {
      "ok": True,
      "message": "Profesor asignado a la materia correctamente"
    }

  except Exception as e:
    return {
      "ok": False,
      "code": 500,
      "message": "Internal Server Error",
      "description": str(e)
    }
  

def remove_professor_from_subject(id_materia, id_profesor):
  try:
    sql = """
      DELETE FROM materia_profesores
      WHERE id_materia = %s
      AND id_usuario = %s
    """

    modify_db(sql, (id_materia, id_profesor))

    return {
      "ok": True,
      "message": "Profesor quitado de la materia correctamente"
    }

  except Exception as e:
    return {
      "ok": False,
      "code": 500,
      "message": "Internal Server Error",
      "description": str(e)
    }
  

def get_subjects_assigned_to_professor(id_profesor):
    try:
        query = """
            SELECT 
                m.id_materia,
                m.nombre,
                m.codigo,
                m.descripcion
            FROM materia_profesores mp
            JOIN materias m ON m.id_materia = mp.id_materia
            WHERE mp.id_usuario = %s
        """

        subjects = query_db(query, (id_profesor,))

        return {
            "ok": True,
            "data": subjects
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }