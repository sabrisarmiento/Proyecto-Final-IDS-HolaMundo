import requests

def course_get_all():
    try:
        response = requests.get('http://localhost:5000/courses')
        if response.status_code == 200:
            return response.json().get('courses', [])
        return []
    except Exception as e:
        print(f'Error: {e}')
        return []
