import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

#NO BORRAR ESTE COMENTARIO, ES PARA USAR POR PRIMERA VEZ
#print(Fernet.generate_key().decode())

load_dotenv()

def get_fernet():
    key = os.getenv("FERNET_KEY")
    return Fernet(key.encode())

def encrypt_value(value):
    if not value:
        return None
    return get_fernet().encrypt(value.encode()).decode()

def decrypt_value(value):
    if not value:
        return None
    return get_fernet().decrypt(value.encode()).decode()