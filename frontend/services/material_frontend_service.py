import requests


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
