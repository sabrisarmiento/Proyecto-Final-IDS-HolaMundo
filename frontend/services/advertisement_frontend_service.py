import requests

class AdvertisementFrontendService:
    @staticmethod
    def get_all(id_curso=None):
        try:
            response = requests.get('http://localhost:5000/advertisements', params={"id_curso": id_curso})
            if response.status_code == 200:
                datos_api = response.json()
                return datos_api.get("advertisements", []) 
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []