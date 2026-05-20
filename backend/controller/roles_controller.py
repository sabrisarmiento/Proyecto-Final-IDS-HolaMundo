from flask import jsonify
from database.db import query_db, modify_db
_FILTER_COLUMNS = {
    "id_roles": "id_roles",
    "name": "nombre",
    "admin_level": "nivel_administracion",
}

def fetch_roles(filters):
    sql = "SELECT * FROM roles"
    condition = " WHERE 1 = 1"
    params = []

    for key, column in _FILTER_COLUMNS.items():
        value = filters.get(key)
        if value:
            sql += f" AND {column} = %s"
            params.append(value)
            
    return query_db(sql + condition, params)

def fetch_rol_by_id(id):
    return query_db("SELECT * FROM roles WHERE id_roles = %s", (id,))

def rol_exists(nombre, nivel):
    return bool(query_db(
        "SELECT id_roles FROM roles WHERE nombre = %s AND nivel_administracion = %s",
        (nombre, nivel),
    ))


def insert_rol(data):
    return modify_db(
        "INSERT INTO roles (nombre, nivel_administracion) VALUES (%s, %s)",
        (data["nombre"], data["nivel_administracion"]),
    )


def delete_rol_by_id(id):
    modify_db("DELETE FROM roles WHERE id_roles = %s", (id,))