import requests

class AttendanceFrontendService:
    @staticmethod
    def get_all():
        try:
            response = requests.get('http://localhost:5000/asistencia')
            if response.status_code == 200:
                datos_api = response.json()
                return datos_api.get("attendance", [])
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []
