import csv, io
from flask import jsonify
from database.db import query_db, modify_db

_FILTER_COLUMNS = {
    "name": "nombre",
    "surname": "apellido",
    "mail": "mail",
    "password": "password",
    "id_rol": "id_rol",
    "created_at": "created_at",
}

def fetch_students(filters):
    sql = "SELECT * FROM alumnos WHERE 1 = 1"
    params = []
    for key, column in _FILTER_COLUMNS.items():
        value = filters.get(key)
        if value:
            sql += f" AND {column} = %s"
            params.append(value)
    return query_db(sql, params)


def fetch_student_by_id(id):
    return query_db("SELECT * FROM alumnos WHERE id_alumno = %s", (id,))


def student_exists_by_email(email):
    return bool(query_db(
        "SELECT id_alumno FROM alumnos WHERE correo = %s", (email,)
    ))


def insert_student(data):
    query = """
        INSERT INTO alumnos (nombre, apellido, correo, password, id_rol)
        VALUES (%s, %s, %s, %s, %s)
    """
    return modify_db(query, (
        data["nombre"],
        data["apellido"],
        data["correo"],
        data["password"],
        data["id_rol"],
    ))