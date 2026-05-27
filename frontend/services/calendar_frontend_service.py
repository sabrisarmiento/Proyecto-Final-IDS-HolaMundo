import requests

class CalendarFrontendService:
    @staticmethod
    def get_all():
        try:
            response = requests.get('http://localhost:5000/clases')
            if response.status_code == 200:
                return response.json().get("classes", []) 
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []