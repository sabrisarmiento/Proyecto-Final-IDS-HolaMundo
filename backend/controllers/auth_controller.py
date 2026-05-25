from database.db import query_db, modify_db
from werkzeug.security import generate_password_hash, check_password_hash
from helpers.validators import validate_login_data, validate_change_password_data
import jwt
import os
from datetime import datetime, timedelta, timezone

def login_user(data):
    try:
        validation = validate_login_data(data)

        if not validation["ok"]:
            return validation
        
        correo = data.get("correo")
        contrasenia = data.get("contraseña")

        result = query_db(
            """
            SELECT id_usuario, nombre, apellido, correo, contraseña, id_rol
            FROM usuarios
            WHERE correo = %s
            """,
            (correo,)
        )

        if not result:
            return {
                "ok": False,
                "code": 401,
                "message": "Unauthorized",
                "description": "Credenciales inválidas"
            }

        user = result[0]

        if not check_password_hash(user["contraseña"], contrasenia):
            return {
                "ok": False,
                "code": 401,
                "message": "Unauthorized",
                "description": "Credenciales inválidas"
            }

        token = jwt.encode({
            "id_usuario": user["id_usuario"],
            "correo": user["correo"],
            "id_rol": user["id_rol"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=2)
        }, os.getenv("SECRET_KEY"), algorithm="HS256")

        return {
            "ok": True,
            "message": "Login exitoso",
            "token": token,
            "user": {
                "id_usuario": user["id_usuario"],
                "nombre": user["nombre"],
                "apellido": user["apellido"],
                "correo": user["correo"],
                "id_rol": user["id_rol"]
            }
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }


def change_password(data, id_usuario):
    try:
        validation = validate_change_password_data(data)

        if not validation["ok"]:
            return validation


        current_password = data.get("current_password")
        new_password = data.get("new_password")

        result = query_db(
            """
            SELECT id_usuario, contraseña
            FROM usuarios
            WHERE id_usuario = %s
            """,
            (id_usuario,)
        )

        if not result:
            return {
                "ok": False,
                "code": 404,
                "message": "Not Found",
                "description": "Usuario no encontrado"
            }

        user = result[0]
        #para cambiar la contraseña el usuario debe saber la contraseña anterior.
        if not check_password_hash(user["contraseña"], current_password):
            return {
                "ok": False,
                "code": 401,
                "message": "Unauthorized",
                "description": "La contraseña actual es incorrecta"
            }
        
        if check_password_hash(user["contraseña"], new_password):
             return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "La nueva contraseña no puede ser igual a la actual"
            }

        hashed_password = generate_password_hash(new_password)

        modify_db(
            """
            UPDATE usuarios
            SET contraseña = %s
            WHERE id_usuario = %s
            """,
            (hashed_password, id_usuario)
        )

        return {
            "ok": True,
            "message": "Contraseña actualizada correctamente"
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }


#def register_user(data):
#    try:
#        nombre = data.get("nombre")
#        apellido = data.get("apellido")
#        correo = data.get("correo")
#        contrasenia = data.get("contraseña")
#        id_rol = data.get("id_rol")

#        if not nombre or not apellido or not correo or not contrasenia or not id_rol:
#            return {
#                "ok": False,
#                "code": 400,
#                "message": "Bad Request",
#                "description": "Nombre, apellido, correo, contraseña e id_rol son obligatorios"
#            }

#        existing_user = query_db(
#            "SELECT id_usuario FROM usuarios WHERE correo = %s",
#            (correo,)
#        )

#        if existing_user:
#            return {
#                "ok": False,
#                "code": 409,
#                "message": "Conflict",
#                "description": "Ya existe un usuario con ese correo"
#            }

#        contrasenia_hash = generate_password_hash(contrasenia)

#        sql = """
#            INSERT INTO usuarios (nombre, apellido, correo, contraseña, id_rol)
#            VALUES (%s, %s, %s, %s, %s)
#        """

#       modify_db(sql, (nombre, apellido, correo, contrasenia_hash, id_rol))

#        return {
#            "ok": True,
#            "message": "Usuario registrado con éxito"
#        }

#    except Exception as e:
#        return {
#            "ok": False,
#            "code": 500,
#            "message": "Internal Server Error",
#            "description": str(e)
#        }
    