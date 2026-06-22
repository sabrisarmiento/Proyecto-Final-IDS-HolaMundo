from database.db import query_db, modify_db
from werkzeug.security import generate_password_hash
from controllers.roles_controller import get_role_by_id
from helpers.admin_permissions import can_manage_admin_level

def get_user_with_admin_level(id_user):
  sql = """
    SELECT 
      u.id_usuario,
      u.id_rol,
      r.nivel_administracion
    FROM usuarios u
    JOIN roles r ON u.id_rol = r.id_rol
    WHERE u.id_usuario = %s
  """

  result = query_db(sql, (int(id_user),))

  if result:
    return result[0]

  return None

def get_all_users(filters):
  try:
    id_usuario = filters.get('id_usuario')
    nombre = filters.get('nombre')
    apellido = filters.get('apellido')
    correo = filters.get('correo')
    creado = filters.get('creado')
    id_rol = filters.get('id_rol')

    sql = """
      SELECT
        id_usuario,
        nombre,
        apellido,
        correo,
        creado,
        id_rol
        FROM usuarios
        """
    condition = " WHERE 1=1"
    params = []

    if id_usuario is not None:
      condition += " AND id_usuario = %s"
      params.append(int(id_usuario))

    if nombre is not None:
      condition += " AND nombre = %s"
      params.append(nombre)

    if apellido is not None:
      condition += " AND apellido = %s"
      params.append(apellido)

    if correo is not None:
      condition += " AND correo = %s"
      params.append(correo)

    if creado is not None:
      condition += " AND creado = %s"
      params.append(creado)

    if id_rol is not None:
      condition += " AND id_rol = %s"
      params.append(int(id_rol))

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

def get_user_by_id(id_user):
  try:
    sql = """
      SELECT
        id_usuario,
        nombre,
        apellido,
        correo,
        creado,
        id_rol
      FROM usuarios
      WHERE id_usuario = %s
    """
    result = query_db(sql, (id_user,))
    if not result:
      return {
        "ok": False,
        "code": 404,
        "message": "Not Found",
        "description": f"No existe un usuario con ID {id_user}"
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

def create_user(data, logged_user):
  try:

    nombre = data.get('nombre')
    apellido = data.get('apellido')
    correo = data.get('correo')
    contraseña = data.get('contraseña')
    id_rol = data.get('id_rol')

    if not nombre or not apellido or not correo or not contraseña or id_rol is None:
      return {
        "ok": False,
        "code": 400,
        "message": "Bad Request",
        "description": "Faltan datos obligatorios"
      }

    rol_to_create = get_role_by_id(id_rol)

    if not rol_to_create:
      return {
        "ok": False,
        "code": 400,
        "message": "Bad Request",
        "description": "El rol indicado no existe"
      }

    nivel_logged_user = logged_user.get("nivel")
    nivel_to_create = rol_to_create.get("nivel_administracion")

    if not can_manage_admin_level(nivel_logged_user, nivel_to_create):
      return {
        "ok": False,
        "code": 403,
        "message": "Forbidden",
        "description": "No tienes permisos para crear un usuario con ese rol"
      }

    sql_check = """
            SELECT id_usuario
            FROM usuarios
            WHERE correo = %s
        """
    
    existing = query_db(sql_check, (correo,))
    
    if existing:
      return {
        "ok": False,
        "code": 409,
        "message": "Conflict",
        "description": "El correo ya está registrado"
      }
    
    password_hash = generate_password_hash(contraseña)

    sql = """
      INSERT INTO usuarios(
        nombre,
        apellido,
        correo,
        contraseña,
        id_rol
      ) VALUES (%s, %s, %s, %s, %s)
    """

    modify_db(sql, (nombre, apellido, correo, password_hash, int(id_rol)))
    return {
      "ok": True,
      "message": "usuario creado correctamente"
    }
  except Exception as e:
    return {
      "ok": False,
      "code": 400,
      "message": "Bad Request",
      "description": str(e)
    }

def update_user_by_id(id_user, data, logged_user):
  try:
    user_to_update = get_user_with_admin_level(id_user)

    if not user_to_update:
      return {
        "ok": False,
        "code": 404,
        "message": "Not Found",
        "description": f"No existe un usuario con ID {id_user} para actualizar"
      }

    nivel_logged_user = logged_user.get("nivel")
    nivel_target = user_to_update.get("nivel_administracion")
    is_self_edit = logged_user.get("id_usuario") == id_user

    if not is_self_edit and not can_manage_admin_level(nivel_logged_user, nivel_target):
      return {
        "ok": False,
        "code": 403,
        "message": "Forbidden",
        "description": "No tienes permisos para modificar este usuario"
      }

    nombre = data.get("nombre")
    apellido = data.get("apellido")
    correo = data.get("correo")
    contraseña = data.get("contraseña")
    id_rol = data.get("id_rol")

    update = []
    params = []

    if nombre is not None:
      update.append("nombre = %s")
      params.append(nombre)

    if apellido is not None:
      update.append("apellido = %s")
      params.append(apellido)

    if correo is not None:
      update.append("correo = %s")
      params.append(correo)

    if contraseña is not None:
      update.append("contraseña = %s")
      params.append(generate_password_hash(contraseña))

    if id_rol is not None:
      if is_self_edit:
        return {
          "ok": False,
          "code": 403,
          "message": "Forbidden",
          "description": "No podés cambiar tu propio rol"
        }
      new_role = get_role_by_id(id_rol)

      if not new_role:
        return {
          "ok": False,
          "code": 400,
          "message": "Bad Request",
          "description": "El rol indicado no existe"
        }
      new_level = new_role.get("nivel_administracion")
      if not can_manage_admin_level(nivel_logged_user, new_level):
        return {
          "ok": False,
          "code": 403,
          "message": "Forbidden",
          "description": "No tienes permisos para asignar ese rol"
        }

      update.append("id_rol = %s")
      params.append(int(id_rol))

    if not update:
      return {
        "ok": False,
        "code": 400,
        "message": "Bad Request",
        "description": "No hay datos para actualizar"
      }

    sql = f"""
      UPDATE usuarios
      SET {', '.join(update)}
      WHERE id_usuario = %s
    """
    params.append(int(id_user))

    modify_db(sql, params)
    return {
      "ok": True,
      "message": "Usuario actualizado con exito",
      "id_usuario": id_user
    }
  except Exception as e:
    return {
      "ok": False,
      "code": 400,
      "message": "Bad Request",
      "description": str(e)
    }

def delete_user_by_id(id_user, logged_user):
  try:
    user_to_delete = get_user_with_admin_level(id_user)

    if not user_to_delete:
      return {
        "ok": False,
        "code": 404,
        "message": "Not Found",
        "description": f"No existe un usuario con ID {id_user} para eliminar"
      }
    nivel_logged_user = logged_user.get("nivel")
    nivel_target = user_to_delete.get("nivel_administracion")

    if not can_manage_admin_level(nivel_logged_user, nivel_target):
      return {
        "ok": False,
        "code": 403,
        "message": "Forbidden",
        "description": "No tienes permisos para eliminar este usuario"
      }
    
    sql = "DELETE FROM usuarios WHERE id_usuario = %s"
    modify_db(sql, (int(id_user),))

    return {
      "ok": True,
      "message": f"Usuario con ID {id_user} eliminado correctamente"
    }
  except Exception as e:
    return {
      "ok": False,
      "code": 500,
      "message": "Internal Server Error",
      "description": str(e)
    }
