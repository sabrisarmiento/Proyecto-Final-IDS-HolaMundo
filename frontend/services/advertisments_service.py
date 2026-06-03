import requests

def get_advertisements():
    """Trae todos los avisos disponibles"""
    try:
        response = requests.get("http://localhost:5000/advertisements")
        response.raise_for_status()
        return response.json().get("advertisements", [])
    except Exception as e:
        print(f"Error al obtener los avisos: {e}")
        return []

def get_advertisements_by_course(id_curso):
    """Trae los avisos de un curso específico"""
    try:
        response = requests.get(
            "http://localhost:5000/advertisements",
            params={"id_curso": id_curso}
        )
        response.raise_for_status()
        return response.json().get("advertisements", [])
    except Exception as e:
        print(f"Error al obtener los avisos del curso {id_curso}: {e}")
        return []
