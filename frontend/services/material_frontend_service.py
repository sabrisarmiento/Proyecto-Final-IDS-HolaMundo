import requests

class MaterialFrontendService:

    @staticmethod
    def get_all(id_curso=None):
        try:

            params = {}

            if id_curso:
                params["id_curso"] = id_curso

            response = requests.get(
                "http://localhost:5000/materials",
                params=params
            )

            if response.status_code == 200:
                datos_api = response.json()
                return datos_api.get("materials", [])

            return []

        except Exception as e:
            print(f"Error: {e}")
            return []