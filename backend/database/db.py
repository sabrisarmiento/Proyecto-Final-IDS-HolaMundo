import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_password = os.getenv("DB_PASSWORD")
db_user = os.getenv("DB_USER")

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": db_user,
    "password": db_password,
    "database": os.getenv("DB_NAME", "DB_ProyectoFinal_IDS"),
    "charset": "utf8mb4",
}

def connect_db():
    conn = mysql.connector.connect(**db_config)
    return conn

def query_db(query, params=None):
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, params or ())
        result = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return result

def modify_db(query, params=None):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(query, params or ())
        connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        connection.close()

def insert_db(query, params=None):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(query, params or ())
        connection.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        connection.close()