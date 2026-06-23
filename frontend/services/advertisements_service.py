import os
import requests

API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000")


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

def get_slack_advertisements_by_course(id_course):
    try:
        response = requests.get(
            f"{API_URL}/courses/{id_course}/slack/messages"
        )

        response.raise_for_status()

        return response.json().get("messages", [])

    except Exception as e:
        print(f"Error al obtener avisos de Slack del curso {id_course}: {e}")
        return []

def get_all_combined_advertisements(id_course=None):
    normal_advertisements = get_advertisements_by_course(id_course)
    slack_advertisements = get_slack_advertisements_by_course(id_course)

    advertisements = normal_advertisements + slack_advertisements

    return advertisements


def create_advertisement(id_course, title, message, token):
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }

        data = {
            "id_curso": id_course,
            "titulo": title,
            "mensaje": message
        }

        response = requests.post(
            f"{API_URL}/advertisements",
            json=data,
            headers=headers
        )
        print("STATUS CREATE AD:", response.status_code)
        print("TEXT CREATE AD:", response.text)
        if response.status_code in [200, 201]:
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
    
def configure_slack_course(id_course, slack_bot_token, slack_channel_id, slack_channel_name, permite_escritura, permite_lectura, token):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        data = {
            "slack_bot_token": slack_bot_token,
            "slack_channel_id": slack_channel_id,
            "slack_channel_name": slack_channel_name,
            "permite_escritura": permite_escritura,
            "permite_lectura": permite_lectura
        }

        response = requests.post(
            f"{API_URL}/courses/{id_course}/slack/config",
            json=data,
            headers=headers
        )

        if response.status_code in [200, 201]:
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
        print(f"Error al configurar Slack: {e}")

        return {
            "ok": False,
            "status_code": 500,
            "data": str(e)
        }

def get_advertisement_by_id(id_advertisement, token):
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(
            f"{API_URL}/advertisements/{id_advertisement}",
            headers=headers
        )

        response.raise_for_status()

        body = response.json()

        return {
            "ok": True,
            "data": body.get("advertisement")
        }

    except Exception as e:
        print(f"Error al obtener el aviso {id_advertisement}: {e}")

        return {
            "ok": False,
            "data": None
        }
  

def update_advertisement(id_advertisement, title, message, token):
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }

        data = {
            "titulo": title,
            "mensaje": message
        }

        response = requests.patch(
            f"{API_URL}/advertisements/{id_advertisement}",
            json=data,
            headers=headers
        )

        print("STATUS UPDATE AD:", response.status_code)
        print("TEXT UPDATE AD:", response.text)

        if response.status_code in [200, 204]:
            return {
                "ok": True,
                "data": response.json() if response.text else None
            }

        return {
            "ok": False,
            "status_code": response.status_code,
            "data": response.json() if response.text else None
        }

    except Exception as e:
        print(f"Error al editar aviso: {e}")

        return {
            "ok": False,
            "status_code": 500,
            "data": str(e)
        }


def delete_advertisement(id_advertisement, token):
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.delete(
            f"{API_URL}/advertisements/{id_advertisement}",
            headers=headers
        )

        print("STATUS DELETE AD:", response.status_code)
        print("TEXT DELETE AD:", response.text)

        if response.status_code in [200, 204]:
            return {
                "ok": True,
                "data": response.json() if response.text else None
            }

        return {
            "ok": False,
            "status_code": response.status_code,
            "data": response.json() if response.text else None
        }

    except Exception as e:
        print(f"Error al eliminar aviso: {e}")

        return {
            "ok": False,
            "status_code": 500,
            "data": str(e)
        }