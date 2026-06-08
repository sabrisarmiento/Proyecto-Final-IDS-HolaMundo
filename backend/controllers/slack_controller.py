import os
import requests
from urllib.parse import urlencode
from database.db import modify_db, query_db


def build_slack_install_url(id_curso, user):
    id_usuario = user["id_usuario"]

    params = {
        "client_id": os.getenv("SLACK_CLIENT_ID"),
        "scope": "chat:write,channels:read,incoming-webhook",
        "redirect_uri": os.getenv("SLACK_REDIRECT_URI"),
        "state": f"{id_curso}:{id_usuario}"
    }

    query_string = urlencode(params)

    return f"https://slack.com/oauth/v2/authorize?{query_string}"


def handle_slack_callback(code, state):
    try:
        if not code or not state:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "Falta code o state"
            }

        state_parts = state.split(":")

        if len(state_parts) != 2:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "State inválido"
            }

        id_curso = int(state_parts[0])
        id_usuario = int(state_parts[1])

        response = requests.post(
            "https://slack.com/api/oauth.v2.access",
            data={
                "code": code,
                "redirect_uri": os.getenv("SLACK_REDIRECT_URI")
            },
            auth=(
                os.getenv("SLACK_CLIENT_ID"),
                os.getenv("SLACK_CLIENT_SECRET")
            )
        )

        data = response.json()

        if not data.get("ok"):
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": data.get("error")
            }

        access_token = data.get("access_token")
        team = data.get("team", {})
        incoming_webhook = data.get("incoming_webhook", {})

        slack_team_id = team.get("id")
        slack_channel_id = incoming_webhook.get("channel_id")
        slack_channel_name = incoming_webhook.get("channel")
        slack_webhook_url = incoming_webhook.get("url")

        sql = """
            INSERT INTO curso_slack_config (
                id_curso,
                slack_team_id,
                slack_channel_id,
                slack_channel_name,
                slack_bot_token,
                slack_webhook_url,
                instalado_por
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                slack_team_id = VALUES(slack_team_id),
                slack_channel_id = VALUES(slack_channel_id),
                slack_channel_name = VALUES(slack_channel_name),
                slack_bot_token = VALUES(slack_bot_token),
                slack_webhook_url = VALUES(slack_webhook_url),
                instalado_por = VALUES(instalado_por)
        """

        modify_db(sql, (
            id_curso,
            slack_team_id,
            slack_channel_id,
            slack_channel_name,
            access_token,
            slack_webhook_url,
            id_usuario
        ))

        return {
            "ok": True,
            "id_curso": id_curso,
            "data": "Slack conectado correctamente"
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }
    
def send_advertisement_to_slack(id_curso, title, message, user_mail):
    try:
        sql = """
            SELECT slack_webhook_url
            FROM curso_slack_config
            WHERE id_curso = %s
        """

        result = query_db(sql, (id_curso,))

        if not result:
            return {
                "ok": True,
                "message": "El curso no tiene Slack configurado"
            }

        webhook_url = result[0].get("slack_webhook_url")

        if not webhook_url:
            return {
                "ok": True,
                "message": "El curso no tiene webhook configurado"
            }

        response = requests.post(
            webhook_url,
            json={
                "text": f"*Nuevo aviso publicado desde Panel FIUBA*\n\n*{title}*\n{message}\n\nPublicado por: {user_mail}"
            }
        )

        print("SLACK STATUS:", response.status_code)
        print("SLACK RESPONSE:", response.text)

        if response.status_code == 200:
            return {
                "ok": True,
                "message": "Aviso enviado a Slack"
            }

        return {
            "ok": False,
            "message": "Slack respondió con error",
            "description": response.text
        }

    except Exception as e:
        print("ERROR ENVIANDO A SLACK:", e)
        return {
            "ok": False,
            "message": "No se pudo enviar a Slack",
            "description": str(e)
        }
    
def disconnect_slack_course(id_curso):
    try:
        sql = """
            DELETE FROM curso_slack_config
            WHERE id_curso = %s
        """

        modify_db(sql, (id_curso,))

        return {
            "ok": True,
            "data": "Slack desconectado correctamente"
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }