from config import BASE_URL, get_headers
import requests

def get_courses():
  try:
    response = requests.get(f'{BASE_URL}/courses', headers=get_headers())
    response.raise_for_status()
    return response.json().get("courses", [])
  except Exception as e:
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

import requests
from config import BASE_URL, get_headers

def post_course(data):
    try:
        response = requests.post(f"{BASE_URL}/courses", json=data, headers=get_headers())
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error al crear curso: {e}")
        return None