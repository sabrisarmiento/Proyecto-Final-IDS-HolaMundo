# import os
# import requests
# from datetime import datetime

# #dejo comwntada esta version (dice publicado por slack y no el usuario correspondiente)
# # def get_slack_advertisements():
# #     token = os.getenv("SLACK_BOT_TOKEN")
# #     channel_id = os.getenv("SLACK_CHANNEL_ID")

# #     if not token or not channel_id:
# #         return {
# #             "ok": False,   
# #             "message": "Faltan variables de entorno de Slack",
# #             "description": "Se deben configurar SLACK_BOT_TOKEN y SLACK_CHANNEL_ID."
# #         }

# #     url = "https://slack.com/api/conversations.history"

# #     headers = {
# #         "Authorization": f"Bearer {token}"
# #     }

# #     params = {
# #         "channel": channel_id,
# #         "limit": 10
# #     }

# #     response = requests.get(url, headers=headers, params=params)
# #     data = response.json()

# #     if not data.get("ok"):
# #         return {
# #             "ok": False,
# #             "message": "No se pudieron obtener los mensajes de Slack",
# #             "description": data.get("error", "Error desconocido de Slack.")
# #         }

# #     advertisements = []

# #     for message in data.get("messages", []):
# #         text = message.get("text", "")
# #         timestamp = float(message.get("ts", 0))
# #         fecha = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")

# #         advertisements.append({
# #             "fecha": fecha,
# #             "emisor": "Slack",
# #             "titulo": "Aviso de Slack",
# #             "mensaje": text
# #         })

# #     return {
# #         "ok": True,
# #         "data": advertisements
# #     }

# def get_slack_user_name(token, user_id):
#     url = "https://slack.com/api/users.info"

#     headers = {
#         "Authorization": f"Bearer {token}"
#     }

#     params = {
#         "user": user_id
#     }

#     response = requests.get(url, headers=headers, params=params)
#     data = response.json()
#     #print("RESPUESTA USERS.INFO:", data)

#     user_name = "Slack"

#     if data.get("ok"):
#         user = data.get("user", {})
#         profile = user.get("profile", {})

#         user_name = (
#             profile.get("display_name")
#             or profile.get("real_name")
#             or user.get("name")
#             or "Slack"
#         )

#     return user_name


# def get_slack_advertisements():
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