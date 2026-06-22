import requests
from datetime import datetime
from database.db import modify_db, query_db
from helpers.crypto import encrypt_value, decrypt_value

def get_slack_user_name(token, user_id):
    url = "https://slack.com/api/users.info"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "user": user_id
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    user_name = "Slack"

    if data.get("ok"):
        user = data.get("user", {})
        profile = user.get("profile", {})

        user_name = (
            profile.get("display_name")
            or profile.get("real_name")
            or user.get("name")
            or "Slack"
        )

    return user_name
    
def send_advertisement_to_slack(id_curso, title, message, user_mail):
    try:
        sql = """
            SELECT slack_bot_token, slack_channel_id, permite_escritura
            FROM curso_slack_config
            WHERE id_curso = %s
        """

        result = query_db(sql, (id_curso,))

        if not result:
            return {
                "ok": True,
                "message": "El curso no tiene Slack configurado"
            }

        config = result[0]

        if not config.get("permite_escritura"):
            return {
                "ok": True,
                "message": "El curso no tiene habilitado poder mandar avisos de la web a slack"
            }
        slack_bot_token = decrypt_value(config.get("slack_bot_token"))
        slack_channel_id = config.get("slack_channel_id")

        if not slack_bot_token or not slack_channel_id:
            return {
                "ok": False,
                "message": "Faltan datos de configuración de Slack"
            }
        
        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={
                "Authorization": f"Bearer {slack_bot_token}",
                "Content-Type": "application/json"
            },
            json={
                "channel": slack_channel_id,
                "text": f"*Nuevo aviso publicado desde Panel FIUBA*\n\n*{title}*\n{message}\n\nPublicado por: {user_mail}"
            }
        )
        data = response.json()

        print("SLACK RESPONSE:", data)

        if data.get("ok"):
            return {
                "ok": True,
                "message": "Aviso enviado a Slack"
            }

        return {
            "ok": False,
            "message": "Slack respondió con error",
            "description": data.get("error")
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
    


def configure_slack_course(id_curso, data, id_usuario):
    try:
        slack_bot_token = data.get("slack_bot_token")
        slack_channel_id = data.get("slack_channel_id")
        slack_channel_name = data.get("slack_channel_name")
        permite_escritura = data.get("permite_escritura", False)
        permite_lectura = data.get("permite_lectura", False)

        if not slack_bot_token or not slack_channel_id:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "Faltan slack_bot_token o slack_channel_id"
            }
        encrypted_slack_bot_token = encrypt_value(slack_bot_token)
        sql = """
            INSERT INTO curso_slack_config (
                id_curso,
                slack_channel_id,
                slack_channel_name,
                slack_bot_token,
                permite_escritura,
                permite_lectura,
                instalado_por
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                slack_channel_id = VALUES(slack_channel_id),
                slack_channel_name = VALUES(slack_channel_name),
                slack_bot_token = VALUES(slack_bot_token),
                permite_escritura = VALUES(permite_escritura),
                permite_lectura = VALUES(permite_lectura),
                instalado_por = VALUES(instalado_por)
        """

        modify_db(sql, (
            id_curso,
            slack_channel_id,
            slack_channel_name,
            encrypted_slack_bot_token,
            permite_escritura,
            permite_lectura,
            id_usuario
        ))

        return {
            "ok": True,
            "data": "Slack configurado correctamente"
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }

def get_slack_messages(id_curso):
    try:
        sql = """
            SELECT 
                slack_bot_token,
                slack_channel_id,
                permite_lectura
            FROM curso_slack_config
            WHERE id_curso = %s
        """

        result = query_db(sql, (id_curso,))

        if not result:
            return {
                "ok": True,
                "data": [],
                "message": "El curso no tiene Slack configurado"
            }

        config = result[0]

        if not config.get("permite_lectura"):
            return {
                "ok": True,
                "data": [],
                "message": "El curso no tiene habilitada la lectura de Slack"
            }

        slack_bot_token = decrypt_value(config.get("slack_bot_token"))
        slack_channel_id = config.get("slack_channel_id")

        if not slack_bot_token or not slack_channel_id:
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": "Faltan slack_bot_token o slack_channel_id"
            }

        response = requests.get(
            "https://slack.com/api/conversations.history",
            headers={
                "Authorization": f"Bearer {slack_bot_token}"
            },
            params={
                "channel": slack_channel_id,
                "limit": 10
            }
        )

        data = response.json()

        if not data.get("ok"):
            return {
                "ok": False,
                "code": 400,
                "message": "Bad Request",
                "description": data.get("error")
            }

        slack_messages = []

        for message in data.get("messages", []):
            ts = message.get("ts")
            fecha = ""

            if ts:
                fecha = datetime.fromtimestamp(float(ts)).strftime("%d/%m/%Y %H:%M")

            if message.get("subtype") == "bot_message" or message.get("bot_id") or message.get("app_id"):
                emisor = "Slack Bot"
                origen = "panel_confirmado"
            else:
                emisor = "Usuario Slack"
                origen = "slack"

            slack_messages.append({
                "titulo": "Mensaje de Slack",
                "mensaje": message.get("text", ""),
                "emisor": emisor,
                "fecha": fecha,
                "origen": origen
            })

        return {
            "ok": True,
            "data": slack_messages
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }