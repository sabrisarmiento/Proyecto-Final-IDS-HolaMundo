from functools import wraps
from flask import request
from helpers.responses import error_response
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

def require_auth(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return error_response({
                "code": 401,
                "message": "Unauthorized",
                "description": "Token requerido"
            })

        try:
            parts = auth_header.split(" ")

            if len(parts) != 2 or parts[0] != "Bearer":
                return error_response({
                    "code": 401,
                    "message": "Unauthorized",
                    "description": "Formato de token inválido"
                })

            token = parts[1]

            payload = jwt.decode(
                token,
                os.getenv("SECRET_KEY"),
                algorithms=["HS256"]
            )

            request.user = payload

        except Exception as e:
            return error_response({
                "code": 401,
                "message": "Unauthorized",
                "description": str(e)
            })

        return function(*args, **kwargs)

    return wrapper


def require_min_role(min_role_id):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            user = getattr(request, "user", None) #Busca request.user. Si no existe, devuelve None.

            if not user:
                return error_response({
                    "code": 401,
                    "message": "Unauthorized",
                    "description": "Usuario no autenticado"
                })
            
            user_role = user.get("id_rol")

            if user_role is None or user_role < min_role_id:
                return error_response({
                    "code": 403,
                    "message": "Forbidden",
                    "description": "No tienes permisos"
                })

            return function(*args, **kwargs)

        return wrapper

    return decorator



#esto seria si solo fueran dos roles, lo dejo por las dudas si cambiamos algo a futuro
#def require_role(role_id):

#    def decorator(function): 

#        @wraps(function) 
#        def wrapper(*args, **kwargs):

#            user = request.user

#            if user["id_rol"] != role_id:
#                return error_response({
#                    "code": 403,
#                    "message": "Forbidden",
#                    "description": "No tienes permisos"
#                })

#           return function(*args, **kwargs)

#        return wrapper

#    return decorator