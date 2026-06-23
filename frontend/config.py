import os
from flask import session

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000")

def get_headers():
    token = session.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}

def get_token():
    return session.get('token')
