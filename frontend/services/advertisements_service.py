import requests

API_URL = "http://localhost:5000"


def get_advertisements():
    try:
        response = requests.get(f"{API_URL}/advertisements")
        response.raise_for_status()

        return response.json().get("advertisements", [])

    except Exception as e:
        print(f"Error al obtener los avisos: {e}")
        return []


def get_advertisements_by_course(id_course):
    try:
        response = requests.get(
            f"{API_URL}/advertisements",
            params={"id_curso": id_course}
        )

        response.raise_for_status()

        return response.json().get("advertisements", [])

    except Exception as e:
        print(f"Error al obtener los avisos del curso {id_course}: {e}")
        return []


def get_advertisements_by_subject(id_subject):
    try:
        response = requests.get(
            f"{API_URL}/advertisements/subject/{id_subject}"
        )

        response.raise_for_status()

        return response.json().get("advertisements", [])

    except Exception as e:
        print(f"Error al obtener avisos de la materia {id_subject}: {e}")
        return []


def get_slack_advertisements():
    try:
        response = requests.get(f"{API_URL}/advertisements/slack")
        response.raise_for_status()

        return response.json().get("advertisements", [])

    except Exception as e:
        print(f"Error al obtener avisos de Slack: {e}")
        return []


def get_all_combined_advertisements(id_course=None):
    normal_advertisements = get_advertisements_by_course(id_course)
    slack_advertisements = get_slack_advertisements()

    advertisements = normal_advertisements + slack_advertisements

    return advertisements


def create_advertisement(id_course, title, message, token):
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }

        body = {
            "id_curso": id_course,
            "titulo": title,
            "mensaje": message
        }

        response = requests.post(
            f"{API_URL}/advertisements",
            json=body,
            headers=headers
        )

        if response.status_code == 201:
            return {
                "ok": True,
                "data": response.json()
            }

        return {
            "ok": False,
            "status_code": response.status_code,
            "data": response.json()
        }

    except Exception as e:
        print(f"Error al crear aviso: {e}")

        return {
            "ok": False,
            "status_code": 500,
            "data": str(e)
        }