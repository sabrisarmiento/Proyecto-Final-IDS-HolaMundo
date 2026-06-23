from config import BASE_URL, get_headers, get_user
from helpers.logger import log_action
import requests

def get_courses():
  try:
    response = requests.get(f'{BASE_URL}/courses', headers=get_headers())
    response.raise_for_status()
    return response.json().get("courses", [])
  except Exception as e:
    return []

def get_my_courses():
    try:
        response = requests.get(f'{BASE_URL}/courses/mias', headers=get_headers())
        response.raise_for_status()
        return response.json().get("courses", [])
    except Exception:
        return []


def get_course_by_id(id):
  try:
    response = requests.get(f'{BASE_URL}/courses/{id}', headers=get_headers())
    response.raise_for_status()
    res_json = response.json()
    return (
            res_json.get("course")
            or res_json.get("data")
            or res_json.get("curso")
            or {}
        )
  except Exception as e:
    return {}

def get_course_by_subject(name):
  try:
    res = requests.get(f"{BASE_URL}/courses", params={"materia": str(name)})
    res.raise_for_status()
    return res.json().get("courses", [])
  except Exception as e:
    return {}

def post_course(data):
    user = get_user()
    try:
        response = requests.post(f"{BASE_URL}/courses", json=data, headers=get_headers())
        response.raise_for_status()
        log_action(
            method='POST',
            description=f'Se creo el curso {data["catedra"]}',
            user_id=user.get('id_usuario', 'desconocido'),
            user_email=user.get('correo', 'desconocido'),
            status_code=response.status_code
        )
        return response.json()
    except Exception as e:
        print(f"Error al crear curso: {e}")
        return None