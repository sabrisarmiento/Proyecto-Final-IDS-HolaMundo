import os
from flask import session

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000")

def get_token():
    return session.get('token')

def auth_headers():
    return {'Authorization': f'Bearer {session.get("token")}'}