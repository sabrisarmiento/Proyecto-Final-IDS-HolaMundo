from database.db import query_db, modify_db
from helpers.user_belongs import user_belongs_to_course
from controllers.slack_controller import send_advertisement_to_slack


def get_all_advertisements(filters):
  try:
    id_user = filters.get("id_usuario")
    id_course = filters.get("id_curso")
    title = filters.get("titulo")
    date = filters.get("fecha")

    sql = """
      SELECT
        a.id_aviso,
        a.id_usuario,
        a.id_curso,
        a.titulo,
        a.mensaje,
        a.fecha,
        CONCAT(u.nombre, ' ', u.apellido) as emisor
      FROM avisos a
      JOIN usuarios u ON a.id_usuario = u.id_usuario
      """
    condition = "WHERE 1=1"
    params = []

    if id_user:
      condition += " AND a.id_usuario = %s"
      params.append(int(id_user))

    if id_course:
      condition += " AND a.id_curso = %s"
      params.append(int(id_course))

    if title is not None:
      condition += " AND titulo = %s"
      params.append(title)

    if date is not None:
      condition += " AND fecha = %s"
      params.append(date)

    result = query_db(sql + " " + condition, params)
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

def get_advertisement_by_id(id_advertisement):
  try:
    sql = """
      SELECT
        id_aviso,
        id_usuario,
        titulo,
        mensaje,
        fecha
      FROM avisos
      WHERE id_usuario = %s
    """
    result = query_db(sql, (id_advertisement,))\
    
    if not result:
      return {
        "ok": False,
        "code": 404,
        "message": "Not Found",
        "description": f"No existe un aviso con ID {id_advertisement}"
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

def create_advertisement(data, user):
  try:
    id_user = user["id_usuario"]
    id_course = data.get("id_curso")
    title = data.get("titulo")
    message = data.get("mensaje")
#    user_mail = user["correo"]
    print("USER DEL TOKEN:", user)
    user_mail = user.get("correo", "Usuario Panel FIUBA")
    
    if not id_course or not title or not message:
      return {
        "ok": False,
        "code": 400,
        "message": "Bad Request",
        "description": "Faltan datos obligatorios"
      }
    if not user_belongs_to_course(id_user, id_course):
      return {
        "ok": False,
        "code": 403,
        "message": "Forbidden",
        "description": "No tenés permisos para crear avisos en este curso"
      }
    sql = """
      INSERT INTO avisos (id_usuario, id_curso, titulo, mensaje)
      VALUES (%s, %s, %s, %s)
    """
    modify_db(sql, (id_user, id_course, title, message))

    slack_result = send_advertisement_to_slack(id_course, title, message, user_mail)
    print("RESULTADO SLACK:", slack_result)

    return {
      "ok": True,
      "data": "aviso creado correctamente",
      "slack": slack_result
    }
  except Exception as e:
    return {
      "ok": False,
      "code": 400,
      "message": "Bad Request",
      "description": str(e)
    }

def patch_advertisement_by_id(id_advertisement, data):
  try:
    id_user = data.get("id_usuario")
    title = data.get("titulo")
    message = data.get("mensaje")
    date = data.get("fecha")

    updates = []
    params = []

    if id_user is not None:
      updates.append("id_usuario = %s")
      params.append(int(id_user))
    if title is not None:
      updates.append("titulo = %s")
      params.append(title)
    if message is not None:
      updates.append("mensaje = %s")
      params.append(message)
    if date is not None:
      updates.append("fecha = %s")
      params.append(date)

    if not updates:
      return {
        "ok": False,
        "code": 400,
        "message": "Bad Request",
        "description": "No se enviaron campos para actualizar"
      }

    sql = f"UPDATE avisos SET {', '.join(updates)} WHERE id_usuario = %s"
    params.append(id_advertisement)

    modify_row = modify_db(sql, params)
    if modify_row == 0:
      return {
        "ok": False,
        "code": 404,
        "message": "Not Found",
        "description": f"No hay un aviso con ID {id_advertisement}"
      }
    
    return {
      "ok": True,
      "data": "aviso actualizado correctamente",
      "id_aviso": id_advertisement
    }
  except Exception as e:
    return {
      "ok": False,
      "code": 400,
      "message": "Bad Request",
      "description": str(e)
    }

def delete_advertisement_by_id(id_advertisement):
  try:
    sql = "DELETE FROM avisos WHERE id_usuario = %s"

    modify_row = modify_db(sql, (id_advertisement,))

    if modify_row == 0:
      return {
        "ok": False,
        "code": 404,
        "message": "Not Found",
        "description": f"No se encontro el aviso con el ID {id_advertisement}"
      }
    return {
      "ok": True,
      "data": f"Aviso con ID {id_advertisement} eliminado correctamente"
    }
  except Exception as e:
    return {
      "ok": False,
      "code": 500,
      "message": "Internal Server Error",
      "description": str(e)
    }

def get_advertisements_by_subject(id_materia):
    try:
        sql = """
            SELECT
                a.id_aviso,
                a.id_usuario,
                a.id_curso,
                a.titulo,
                a.mensaje,
                a.fecha,
                CONCAT(u.nombre, ' ', u.apellido) as emisor
            FROM avisos a
            JOIN usuarios u ON a.id_usuario = u.id_usuario
            JOIN cursos c ON a.id_curso = c.id_curso
            WHERE c.id_materia = %s
        """
        result = query_db(sql, (id_materia,))
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