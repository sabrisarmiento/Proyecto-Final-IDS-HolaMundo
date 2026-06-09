import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_password = os.getenv("DB_PASSWORD")
db_user = os.getenv("DB_USER")

db_config = {
    "host": "localhost",
    "user": db_user,
    "password": db_password,
    "database": "DB_ProyectoFinal_IDS"
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