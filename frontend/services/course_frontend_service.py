from config import BASE_URL
import requests

def course_get_all():
    try:
        response = requests.get(f"{BASE_URL}/courses")
        if response.status_code == 200:
            return response.json().get('courses', [])
        return []
    except Exception as e:
        print(f'Error: {e}')
        return []
    
class CourseFrontendService:

    @staticmethod
    def get_all():
        try:
            response = requests.get(f"{BASE_URL}/courses")
            if response.status_code == 200:
                return response.json().get("courses", [])
            return []
        except Exception as e:
            print(f"ERROR get_all: {e}")
            return []

    @staticmethod
    def get_by_id(id_course):
        try:
            response = requests.get(f"{BASE_URL}/courses/{id_course}")
            if response.status_code == 200:
                return response.json().get("course", {})
            return {}
        except Exception as e:
            print(f"ERROR get_by_id: {e}")
            return {}
