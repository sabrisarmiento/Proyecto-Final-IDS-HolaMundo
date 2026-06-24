from config import BASE_URL, get_headers, get_user
from helpers.logger import log_action

import requests

def post_student(data):
    user=get_user()
    try:
        response = requests.post(f'{BASE_URL}/students',  json=data, headers=get_headers())
        response.raise_for_status()
        log_action(
            method='POST',
            description=f'Se creo el estudiante {data["nombre"]} {data["apellido"]}',
            user_id=user.get('id_usuario', 'desconocido'),
            user_email=user.get('correo', 'desconocido'),
            status_code=response.status_code
        )
    except Exception as e:
        return {}
    
def patch_student(student_id, data):
    user=get_user()
    try:
        response = requests.patch(f"{BASE_URL}/students/{student_id}", json=data, headers=get_headers())
        response.raise_for_status()
        log_action(
            method='PATCH',
            description=f'Se actualizo el estudiante {data["nombre"]} {data["apellido"]}',
            user_id=user.get('id_usuario', 'desconocido'),
            user_email=user.get('correo', 'desconocido'),
            status_code=response.status_code
        )
        return response.json()
    except Exception as e:
        print(f"Error al modificar alumno: {e}")
        return None