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
    sql_validation = "SELECT id_materia FROM materias WHERE codigo = %s"
    exists = query_db(sql_validation, (data["codigo"],), one=True)
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
    if exists:
      return {
        "ok": False,
        "code": 409,
        "message": "Conflict",
        "description": f"Ya existe una materia con el código {data['codigo']}"
      }
    
    sql = "INSERT INTO materias (nombre, codigo) VALUES (%s, %s)"
    modify_db(sql, (data["nombre"], data["codigo"]))
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
