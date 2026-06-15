import requests
from database.db import modify_db, query_db


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
    #print("RESPUESTA USERS.INFO:", data)

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


# def get_slack_advertisements(id_curso):
#     sql = """
#         SELECT 
#             slack_bot_token,
#             slack_channel_id,
#             permite_lectura
#         FROM curso_slack_config
#         WHERE id_curso = %s
#     """

#     result = query_db(sql, (id_curso,))

#     if not result:
#         return {
#             "ok": True,
#             "data": [],
#             "message": "El curso no tiene Slack configurado"
#         }
#     config = result[0]

#     if not config.get("permite_lectura"):
#         return {
#             "ok": True,
#             "data": [],
#             "message": "El curso no tiene habilitada la lectura de Slack"
#         }

#     token = config.get("slack_bot_token")
#     channel_id = config.get("slack_channel_id")

#     if not token or not channel_id:
#         return {
#             "ok": False,
#             "message": "Faltan datos de Slack",
#             "description": "Se deben configurar slack_bot_token y slack_channel_id."
#         }
    
#     url = "https://slack.com/api/conversations.history"

#     headers = {
#         "Authorization": f"Bearer {token}"
#     }

#     params = {
#         "channel": channel_id,
#         "limit": 10
#     }

#     response = requests.get(url, headers=headers, params=params)
#     data = response.json()

#     if not data.get("ok"):
#         return {
#             "ok": False,
#             "message": "No se pudieron obtener los mensajes de Slack",
#             "description": data.get("error", "Error desconocido de Slack.")
#         }

#     advertisements = []

#     for message in data.get("messages", []):
#         #print("MENSAJE COMPLETO:", message)
#         text = message.get("text", "")

#         #if text != "":
#         #    timestamp = float(message.get("ts", 0))
#         #    fecha = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")

#         if text != "" and not message.get("subtype"):
#             user_id = message.get("user")
#             emisor = "Slack"

#             #print("USER ID:", user_id)

#             if user_id:
#                 emisor = get_slack_user_name(token, user_id)

#             #print("EMISOR FINAL:", emisor)

#             timestamp = float(message.get("ts", 0))
#             fecha = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")

#             advertisements.append({
#                 "fecha": fecha,
#                 "emisor": emisor,
#                 "titulo": "Aviso de Slack",
#                 "mensaje": text,
#                 "origen": "slack"
#             })

#     return {
#         "ok": True,
#         "data": advertisements
#     }
    
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
        slack_bot_token = config.get("slack_bot_token")
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
            slack_bot_token,
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

        slack_bot_token = config.get("slack_bot_token")
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
            if message.get("subtype") == "bot_message":
                emisor = "Slack Bot"
            else:
                emisor = message.get("user", "Usuario Slack")

            slack_messages.append({
                "titulo": "Mensaje de Slack",
                "mensaje": message.get("text", ""),
                "emisor": emisor,
                "fecha": message.get("ts"),
                "origen": "slack"
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