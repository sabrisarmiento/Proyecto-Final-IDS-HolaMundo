#borrar

import requests

def get_advertisements():
    try:
        response = requests.get("http://127.0.0.1:5000/advertisements")
        response.raise_for_status()
        return response.json().get("advertisements", [])
    except Exception as e:
        print(f"Error al obtener los avisos: {e}")
        return []

def get_advertisements_by_course(id_course):
    try:
        res = requests.get(
            "http://127.0.0.1:5000/advertisements",
            params={"id_curso": id_course}
        )
        res.raise_for_status()
        return res.json().get("advertisements", [])
    except Exception as e:
        print(f"Error al obtener los avisos del curso {id_course}: {e}")
        return []
    
def get_advertisements_by_subject(id_subject):
    try:
        response = requests.get(f"http://127.0.0.1:5000/advertisements/subject/{id_subject}")
        response.raise_for_status()
        return response.json().get("advertisements", [])
    except Exception as e:
        print(f"Error al obtener avisos de la materia {id_subject}: {e}")
        return []
