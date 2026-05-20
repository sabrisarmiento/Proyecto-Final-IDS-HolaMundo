from flask import jsonify
from database.db import query_db, modify_db


def list_users(id_usuario, nombre, apellido, correo, created_at, id_rol):

    sql = """
    SELECT
        id_usuario,
        nombre_usuario,
        apellido_usuario,
        correo_usuario,
        created_at,
        id_rol
    FROM usuarios
    """

    condition = " WHERE 1 = 1"

    params = []

    if id_usuario:
        condition += """
        AND id_usuario = %s
        """
        params.append(id_usuario)

    if nombre:
        condition += """
        AND nombre_usuario = %s
        """
        params.append(nombre)

    if apellido:
        condition += """
        AND apellido_usuario = %s
        """
        params.append(apellido)
    if correo:
        condition += " AND correo_usuario = %s"
        params.append(correo)

    if created_at:
        condition += " AND created_at = %s"
        params.append(created_at)

    if id_rol:
        condition += """
        AND id_rol = %s
        """
        params.append(id_rol)

    return query_db(
        sql + condition,
        params
    )

def get_user(id_usuario):

    try:

        query = """
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

        user = query_db(
            query,
            (id_usuario,)
        )

        if not user:

            return jsonify({
                "errors":[{
                    "code":"404",
                    "message":"Not Found",
                    "level":"error",
                    "description":"No existe un usuario con el ID proporcionado"
                }]
            }), 404

        return jsonify(user[0]), 200

    except Exception as e:

        return jsonify({
            "errors":[{
                "code":"500",
                "message":"Internal Server Error",
                "level":"error",
                "description":str(e)
            }]
        }), 500

def create_user(data):

    try:

        if not data:

            return jsonify({
                "errors":[{
                    "code":"400",
                    "message":"Bad Request",
                    "level":"error",
                    "description":"JSON requerido"
                }]
            }), 400

        query_check = """
            SELECT id_usuario
            FROM usuarios
            WHERE correo_usuario = %s
        """

        existance = query_db(
            query_check,
            (
                data["correo_usuario"],
            )
        )

        if existance:

            return jsonify({
                "errors":[{
                    "code":"409",
                    "message":"Conflict",
                    "level":"error",
                    "description":"El correo ya existe"
                }]
            }), 409

        query_insert = """
            INSERT INTO usuarios(
                nombre_usuario,
                apellido_usuario,
                correo_usuario,
                contraseña,
                id_rol
            )

            VALUES(
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """

        user_id = modify_db(
            query_insert,
            (
                data["nombre_usuario"],
                data["apellido_usuario"],
                data["correo_usuario"],
                data["contraseña"],
                data["id_rol"]
            )
        )

        return jsonify({
            "mensaje":"El usuario ha sido creado exitosamente",
            "id":user_id
        }), 201

    except Exception as e:

        return jsonify({
            "errors":[{
                "code":"500",
                "message":"Internal Server Error",
                "level":"error",
                "description":str(e)
            }]
        }), 500
    
def update_user(id_usuario, data):

    try:

        if not data:

            return jsonify({
                "errors":[{
                    "code":"400",
                    "message":"Bad Request",
                    "level":"error",
                    "description":"JSON requerido"
                }]
            }), 400

        query_check = """
            SELECT *
            FROM usuarios
            WHERE id_usuario = %s
        """

        existance = query_db(
            query_check,
            (id_usuario,)
        )

        if not existance:

            return jsonify({
                "errors":[{
                    "code":"404",
                    "message":"Not Found",
                    "level":"error",
                    "description":"Usuario no encontrado"
                }]
            }), 404

        query_update = """
            UPDATE usuarios

            SET
                nombre_usuario = %s,
                apellido_usuario = %s,
                correo_usuario = %s,
                contraseña = %s,
                id_rol = %s

            WHERE id_usuario = %s
        """

        modify_db(
            query_update,
            (
                data["nombre_usuario"],
                data["apellido_usuario"],
                data["correo_usuario"],
                data["contraseña"],
                data["id_rol"],
                id_usuario
            )
        )

        return jsonify({
            "mensaje":"Usuario actualizado exitosamente"
        }), 200

    except Exception as e:

        return jsonify({
            "errors":[{
                "code":"500",
                "message":"Internal Server Error",
                "level":"error",
                "description":str(e)
            }]
        }), 500

def delete_user(id_usuario):

    try:

        query_check = """
            SELECT *
            FROM usuarios
            WHERE id_usuario = %s
        """

        existance = query_db(
            query_check,
            (id_usuario,)
        )

        if not existance:

            return jsonify({
                "errors":[{
                    "code":"404",
                    "message":"Not Found",
                    "level":"error",
                    "description":"No existe un usuario con el ID proporcionado"
                }]
            }), 404

        query_delete = """
            DELETE FROM usuarios
            WHERE id_usuario = %s
        """

        modify_db(
            query_delete,
            (id_usuario,)
        )

        return '', 204

    except Exception as e:

        return jsonify({
            "errors":[{
                "code":"500",
                "message":"Internal Server Error",
                "level":"error",
                "description":str(e)
            }]
        }), 500
