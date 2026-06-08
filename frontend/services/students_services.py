from config import BASE_URL, get_headers
import requests

def post_student(data):
    try:
        response = requests.post(f'{BASE_URL}/students',  json=data, headers=get_headers())
        response.raise_for_status()
    except Exception as e:
        return {}
    
def patch_student(student_id, data):
    try:
        response = requests.patch(f"{BASE_URL}/students/{student_id}", json=data, headers=get_headers())
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error al modificar alumno: {e}")
        return None