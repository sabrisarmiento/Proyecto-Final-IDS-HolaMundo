from flask import session

BASE_URL = "http://localhost:5000"

def get_headers():
    token = session.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}