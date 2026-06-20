import requests
from config import BASE_URL, get_headers

def get_subjects():
  try:
    response = requests.get(f"{BASE_URL}/subjects")
    response.raise_for_status()
    return response.json().get("subjects", [])
  except Exception as e:
    print(f"Error al obtener las materias: {e}")
    return []

def get_my_subjects():
    try:
        response = requests.get(f"{BASE_URL}/subjects/mias", headers=get_headers())
        response.raise_for_status()
        return response.json().get("subjects", [])
    except Exception:
        return []

def get_subject_by_id(id_materia):
    try:
        response = requests.get(f"{BASE_URL}/subjects/{id_materia}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error al obtener la materia {id_materia}: {e}")
        return []

def get_topics_by_subject_id(id_materia):
    try:
        response = requests.get(f"{BASE_URL}/subjects/{id_materia}/temas")
        response.raise_for_status()
        return response.json().get("temas", [])
    except Exception as e:
        print(f"Error al obtener temas de la materia {id_materia}: {e}")
        return []

def get_subject_by_name(name):
  try:
    res = requests.get(f"{BASE_URL}/subjects", params={"nombre": str(name)})
    res.raise_for_status()
    return res.json()
  except Exception as e:
    print(f"Error al obtener la materia {name}: {e}")
    return {}