from flask import jsonify
from database.db import query_db, modify_db

def get_all_users(filters):
  try:
    id_usuario = filters.get('id_usuario')
    nombre = filters.get('nombre')
    apellido = filters.get('apellido')
    correo = filters.get('correo')
    created_at = filters.get('created_at')
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

    if id_usuario:
      condition += " AND id_usuario = %s"
      params.append(int(id_usuario))

    if nombre:
      condition += " AND nombre_usuario = %s"
      params.append(nombre)

    if apellido:
      condition += " AND apellido_usuario = %s"
      params.append(apellido)

    if correo:
      condition += " AND correo_usuario = %s"
      params.append(correo)

    if created_at:
      condition += " AND created_at = %s"
      params.append(created_at)

    if id_rol:
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

def get_user_by_id(id_usuario):
  try:
    sql = """
      SELECT
        id_usuario,
        nombre_usuario,
        apellido_usuario,
        correo_usuario,
        created_at,
        id_rol
      FROM usuarios
      WHERE id_usuario = %s
    """
    result = query_db(sql, (id_usuario,))
    if not result:
      return {
        "ok": False,
        "code": 404,
        "message": "Not Found",
        "description": f"No existe un usuario con ID {id_usuario}"
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

def create_user(data):
  try:

    nombre = data.get('nombre')
    apellido = data.get('apellido')
    correo = data.get('correo')
    contraseña = data.get('contraseña')
    id_rol = data.get('id_rol')

    sql_check = """
            SELECT id_usuario
            FROM usuarios
            WHERE correo_usuario = %s
        """
    
    existing = query_db(sql_check, (correo,))
    
    if existing:
      return {
        "ok": False,
        "code": 409,
        "message": "Conflict",
        "description": "El correo ya está registrado"
      }

    sql = """
      INSERT INTO usuarios(
        nombre,
        apellido,
        correo,
        contraseña,
        id_rol
      ) VALUES (%s, %s, %s, %s, %s)
    """

    modify_db(sql, (nombre, apellido, correo, contraseña, int(id_rol)))
    return {
      "ok": True,
    }
  except Exception as e:
    return {
      "ok": False,
      "code": 400,
      "message": "Bad Request",
      "description": str(e)
    }

def update_user_by_id(id_usuario, data):
  try:
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    correo = data.get("correo")
    contraseña = data.get("contraseña")
    id_rol = data.get("id_rol") #se debe modificar el rol?

    update = []
    params = []

    if nombre is not None:
      update.append("nombre_usuario = %s")
      params.append(nombre)

    if apellido is not None:
      update.append("apellido_usuario = %s")
      params.append(apellido)

    if correo is not None:
      update.append("correo_usuario = %s")
      params.append(correo)

    if contraseña is not None:
      update.append("contraseña = %s")
      params.append(contraseña)

    if id_rol is not None:
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
    params.append(int(id_usuario))

    modify_row = modify_db(sql, params)
    if modify_row == 0:
      return {
        "ok": False,
        "code": 404,
        "message": "Not Found",
        "description": f"No existe un usuario con ID {id_usuario} para actualizar"
      }
    return {
      "ok": True,
      "message": "Usuario actualizado con exito",
      "id_usuario": id_usuario
    }
  except Exception as e:
    return {
      "ok": False,
      "code": 400,
      "message": "Bad Request",
      "description": str(e)
    }

def delete_user_by_id(id_usuario):
  try:
    sql = "DELETE FROM usuarios WHERE id_usuario = %s"
    modify_row = modify_db(sql, (id_usuario,))
    if modify_row == 0:
      return {
        "ok": False,
        "code": 404,
        "message": "Not Found",
        "description": f"No existe un usuario con ID {id_usuario} para eliminar"
      }
    return {
      "ok": True,
      "message": f"Usuario con ID {id_usuario} eliminado correctamente"
    }
  except Exception as e:
    return {
      "ok": False,
      "code": 500,
      "message": "Internal Server Error",
      "description": str(e)
    }

# def list_users(id_usuario, nombre, apellido, correo, created_at, id_rol):

#     sql = """
#     SELECT
#         id_usuario,
#         nombre_usuario,
#         apellido_usuario,
#         correo_usuario,
#         created_at,
#         id_rol
#     FROM usuarios
#     """

#     condition = " WHERE 1 = 1"

#     params = []

#     if id_usuario:
#         condition += """
#         AND id_usuario = %s
#         """
#         params.append(id_usuario)

#     if nombre:
#         condition += """
#         AND nombre_usuario = %s
#         """
#         params.append(nombre)

#     if apellido:
#         condition += """
#         AND apellido_usuario = %s
#         """
#         params.append(apellido)
#     if correo:
#         condition += " AND correo_usuario = %s"
#         params.append(correo)

#     if created_at:
#         condition += " AND created_at = %s"
#         params.append(created_at)

#     if id_rol:
#         condition += """
#         AND id_rol = %s
#         """
#         params.append(id_rol)

#     return query_db(
#         sql + condition,
#         params
#     )

# def get_user(id_usuario):

#     try:

#         query = """
#         SELECT
#             id_usuario,
#             nombre_usuario,
#             apellido_usuario,
#             correo_usuario,
#             created_at,
#             id_rol
#         FROM usuarios
#         WHERE id_usuario = %s
#         """

#         user = query_db(
#             query,
#             (id_usuario,)
#         )

#         if not user:

#             return jsonify({
#                 "errors":[{
#                     "code":"404",
#                     "message":"Not Found",
#                     "level":"error",
#                     "description":"No existe un usuario con el ID proporcionado"
#                 }]
#             }), 404

#         return jsonify(user[0]), 200

#     except Exception as e:

#         return jsonify({
#             "errors":[{
#                 "code":"500",
#                 "message":"Internal Server Error",
#                 "level":"error",
#                 "description":str(e)
#             }]
#         }), 500

# def create_user(data):

#     try:

#         if not data:

#             return jsonify({
#                 "errors":[{
#                     "code":"400",
#                     "message":"Bad Request",
#                     "level":"error",
#                     "description":"JSON requerido"
#                 }]
#             }), 400

#         query_check = """
#             SELECT id_usuario
#             FROM usuarios
#             WHERE correo_usuario = %s
#         """

#         existance = query_db(
#             query_check,
#             (
#                 data["correo_usuario"],
#             )
#         )

#         if existance:

#             return jsonify({
#                 "errors":[{
#                     "code":"409",
#                     "message":"Conflict",
#                     "level":"error",
#                     "description":"El correo ya existe"
#                 }]
#             }), 409

#         query_insert = """
#             INSERT INTO usuarios(
#                 nombre_usuario,
#                 apellido_usuario,
#                 correo_usuario,
#                 contraseña,
#                 id_rol
#             )

#             VALUES(
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s
#             )
#         """

#         user_id = modify_db(
#             query_insert,
#             (
#                 data["nombre_usuario"],
#                 data["apellido_usuario"],
#                 data["correo_usuario"],
#                 data["contraseña"],
#                 data["id_rol"]
#             )
#         )

#         return jsonify({
#             "mensaje":"El usuario ha sido creado exitosamente",
#             "id":user_id
#         }), 201

#     except Exception as e:

#         return jsonify({
#             "errors":[{
#                 "code":"500",
#                 "message":"Internal Server Error",
#                 "level":"error",
#                 "description":str(e)
#             }]
#         }), 500

# def update_user(id_usuario, data):

#     try:

#         if not data:

#             return jsonify({
#                 "errors":[{
#                     "code":"400",
#                     "message":"Bad Request",
#                     "level":"error",
#                     "description":"JSON requerido"
#                 }]
#             }), 400

#         query_check = """
#             SELECT *
#             FROM usuarios
#             WHERE id_usuario = %s
#         """

#         existance = query_db(
#             query_check,
#             (id_usuario,)
#         )

#         if not existance:

#             return jsonify({
#                 "errors":[{
#                     "code":"404",
#                     "message":"Not Found",
#                     "level":"error",
#                     "description":"Usuario no encontrado"
#                 }]
#             }), 404

#         query_update = """
#             UPDATE usuarios

#             SET
#                 nombre_usuario = %s,
#                 apellido_usuario = %s,
#                 correo_usuario = %s,
#                 contraseña = %s,
#                 id_rol = %s

#             WHERE id_usuario = %s
#         """

#         modify_db(
#             query_update,
#             (
#                 data["nombre_usuario"],
#                 data["apellido_usuario"],
#                 data["correo_usuario"],
#                 data["contraseña"],
#                 data["id_rol"],
#                 id_usuario
#             )
#         )

#         return jsonify({
#             "mensaje":"Usuario actualizado exitosamente"
#         }), 200

#     except Exception as e:

#         return jsonify({
#             "errors":[{
#                 "code":"500",
#                 "message":"Internal Server Error",
#                 "level":"error",
#                 "description":str(e)
#             }]
#         }), 500

# def delete_user(id_usuario):

#     try:

#         query_check = """
#             SELECT *
#             FROM usuarios
#             WHERE id_usuario = %s
#         """

#         existance = query_db(
#             query_check,
#             (id_usuario,)
#         )

#         if not existance:

#             return jsonify({
#                 "errors":[{
#                     "code":"404",
#                     "message":"Not Found",
#                     "level":"error",
#                     "description":"No existe un usuario con el ID proporcionado"
#                 }]
#             }), 404

#         query_delete = """
#             DELETE FROM usuarios
#             WHERE id_usuario = %s
#         """

#         modify_db(
#             query_delete,
#             (id_usuario,)
#         )

#         return '', 204

#     except Exception as e:

#         return jsonify({
#             "errors":[{
#                 "code":"500",
#                 "message":"Internal Server Error",
#                 "level":"error",
#                 "description":str(e)
#             }]
#         }), 500
