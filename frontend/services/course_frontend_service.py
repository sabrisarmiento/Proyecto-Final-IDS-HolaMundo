import requests

class CourseFrontendService:

    @staticmethod
    def get_all():
        try:
            response = requests.get("http://127.0.0.1:5000/courses")

            data = response.json()

            return data.get("courses", [])

        except Exception as e:
            print("ERROR get_all:", e)
            return []

    @staticmethod
    def get_by_id(id_course):
        try:
            response = requests.get(f"http://127.0.0.1:5000/courses/{id_course}")
            data = response.json()

            return data.get("course", {})

        except Exception as e:
            print("ERROR get_by_id:", e)
            return {}