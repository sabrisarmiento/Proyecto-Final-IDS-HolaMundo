import requests
BASE = "http://127.0.0.1:5000"

def attendance_get_all(id_clase=None):
    try:
        params = {"id_clase": id_clase} if id_clase else {}
        r = requests.get(f"{BASE}/asistencia", params=params)
        return r.json().get("attendance", []) if r.status_code == 200 else []
    except Exception as e:
        print(f"Error: {e}")
        return []

def generate_qr(id_clase):
    try:
        r = requests.post(f"{BASE}/asistencia/generar-qr", json={"id_clase": id_clase})
        return r.json()
    except Exception as e:
        print(f"Error: {e}")
        return []
