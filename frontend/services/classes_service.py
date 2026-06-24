import requests
from config import BASE_URL, get_headers, get_user
from helpers.logger import log_action

def get_classes_by_course(course_id):
    try:
        response = requests.get(f'{BASE_URL}/clases', params={'id_curso': course_id})
        body = response.json() if response.content else {}
        
        if response.status_code == 200:
            return {
                "ok": True,
                "data": body.get("classes", [])
            }
        return {
            "ok": False,
            "description": "Error al obtener las clases"
        }
    except Exception as e:
        return {
            "ok": False,
            "description": str(e)
        }

def post_clase(data):
    user=get_user()
    try:
        response = requests.post(f'{BASE_URL}/clases', json=data, headers=get_headers())
        log_action(
            method='POST',
            description=f'Se creo la clase de {data["temas"]} para el curso {data["id_curso"]}',
            user_id=user.get('id_usuario', 'desconocido'),
            user_email=user.get('correo', 'desconocido'),
            status_code=response.status_code
        )
        if response.status_code == 201:
            return {"ok": True}
        return {
            "ok": False,
            "description": "Error al crear la clase"
        }
    except Exception as e:
        return {
            "ok": False,
            "description": str(e)
        }

def patch_clase(id_clase, data):
    user=get_user()
    try:
        response = requests.patch(f'{BASE_URL}/clases/{id_clase}', json=data, headers=get_headers())
        log_action(
            method='PATCH',
            description=f'Se actualizo la clase {id_clase}',
            user_id=user.get('id_usuario', 'desconocido'),
            user_email=user.get('correo', 'desconocido'),
            status_code=response.status_code
        )
        if response.status_code == 200:
            return {"ok": True}
        return {
            "ok": False,
            "description": "Hubo un error al actualizar la clase"
        }
    except Exception as e:
        return {
            "ok": False,
            "description": str(e)
        }

def delete_clase(id_clase):
    user=get_user()
    try:
        response = requests.delete(f'{BASE_URL}/clases/{id_clase}', headers=get_headers())
        log_action(
            method='DELETE',
            description=f'Se elimino la clase {id_clase}',
            user_id=user.get('id_usuario', 'desconocido'),
            user_email=user.get('correo', 'desconocido'),
            status_code=response.status_code
        )
        return {"ok": response.status_code in (200, 204)}
    except Exception as e:
        return {
            "ok": False,
            "description": str(e)
        }