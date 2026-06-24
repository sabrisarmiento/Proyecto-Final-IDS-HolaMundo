from config import BASE_URL, get_headers, get_user
from helpers.logger import log_action
import requests

def patch_user(id, data):
    try:
        response = requests.patch(f'{BASE_URL}/dashboard/usuarios/{id}', json=data, headers=get_headers())

        if response.status_code == 200:
            return {
                "ok": True,
                "data": response.json() if response.content else {}
            }
        else:
            body = response.json() if response.content else {}
            desc = (body.get('errors') or [{}])[0].get('description', 'No se pudo actualizar el usuario')
            return {
                "ok": False,
                "description": desc
            }
    except Exception as e:
        return {
            "ok": False,
            "description": str(e)
        }

def patch_user2(id, data):
    user=get_user()
    try:
        response = requests.patch(f'{BASE_URL}/users/{id}', json=data, headers=get_headers())
        log_action(
            method='PATCH',
            description=f'Se actualizo el usuario de {data["nombre"]} y correo {data["correo"]}',
            user_id=user.get('id_usuario', 'desconocido'),
            user_email=user.get('correo', 'desconocido'),
            status_code=response.status_code
        )
        if response.status_code == 200:
            return {
                "ok": True,
                "data": response.json() if response.content else {}
            }
        else:
            body = response.json() if response.content else {}
            desc = (body.get('errors') or [{}])[0].get('description', 'No se pudo actualizar el perfil')
            return {
                "ok": False,
                "description": desc
            }
    except Exception as e:
        return {
            "ok": False,
            "description": str(e)
        }

def put_password_user(data):
    user = get_user()
    try:
        response = requests.put(f'{BASE_URL}/change-password', json=data, headers=get_headers())
        body = response.json() if response.content else {}
        log_action(
            method='PUT',
            description=f'Se actualizo la contraseña del usuario de {user.get("correo")}',
            user_id=user.get('id_usuario', 'desconocido'),
            user_email=user.get('correo', 'desconocido'),
            status_code=response.status_code
        )
        if response.status_code == 200:
            return {
                "ok": True,
                "message": body.get('message', 'Contraseña actualizada correctamente')
            }
        else:
            desc = (body.get('errors') or [{}])[0].get('description', 'No se pudo cambiar la contraseña')
            return {
                "ok": False,
                "description": desc
            }
    except Exception as e:
        return {
            "ok": False,
            "description": str(e)
        }

def login_user(correo, contraseña):
    try:
        response = requests.post(f'{BASE_URL}/login', json={
            "correo": correo,
            "contraseña": contraseña
        })
        body = response.json() if response.content else {}
        if response.status_code == 200:
            return {
                "ok": True,
                "token": body.get('token'),
                "user": body.get('user')
            }
        else:
            desc = (body.get('errors') or [{}])[0].get('description', 'Credenciales inválidas')
            return {
                "ok": False,
                "description": desc
            }
    except Exception as e:
        return {
            "ok": False,
            "description": "Error de conexión"
        }