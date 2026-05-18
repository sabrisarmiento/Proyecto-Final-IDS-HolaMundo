import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": 1234,
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
        return cursor.lastrowid
    finally:
        cursor.close()
        connection.close()