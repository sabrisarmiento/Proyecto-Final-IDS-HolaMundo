from config import BASE_URL, get_headers
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
    try:
        response = requests.patch(f'{BASE_URL}/users/{id}', json=data, headers=get_headers())

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
    try:
        response = requests.put(f'{BASE_URL}/change-password', json=data, headers=get_headers())
        body = response.json() if response.content else {}

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