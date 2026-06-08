from config import BASE_URL, get_headers
import requests

def get_exams_by_course_id(course_id):
    try:
        response = requests.get(
            f'{BASE_URL}/evaluaciones',
            params={'id_curso': course_id},
            headers=get_headers()
        )
        response.raise_for_status()
        res_json = response.json()
        return (
            res_json.get('evaluaciones')
            or res_json.get('exams')
            or []
        )
    except Exception as e:
        return []