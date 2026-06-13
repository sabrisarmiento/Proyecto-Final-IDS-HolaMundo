import requests
from config import BASE_URL, get_headers


def material_get_all():
    try:
        response = requests.get('http://127.0.0.1:5000/materials')
        if response.status_code == 200:
            datos_api = response.json()
            return datos_api.get("materials", [])
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_materials_by_course(id_curso):
    try:
        response = requests.get(f"{BASE_URL}/materials", params={"id_curso": id_curso})
        response.raise_for_status()
        return response.json().get("materials", [])
    except Exception:
        return []


def create_material(data):
    try:
        response = requests.post(f"{BASE_URL}/materials", json=data, headers=get_headers())
        return response.json(), response.status_code
    except Exception as e:
        return {"errors": [{"description": str(e)}]}, 502
