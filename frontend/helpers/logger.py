import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs', 'activity.log')
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def log_action(method, description, user_id, user_email, status_code):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"{timestamp}|{method}|{description}|{user_id}|{user_email}|{status_code}\n"
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(line)