from flask import jsonify
from database.db import query_db
def mostrar_roles(id_roles, nombre, nivel_administracion):
    sql = "SELECT * FROM partidos"
    condition = "WHERE 1 = 1"
    params = []

    if id_roles:
        condition += " AND fecha %s"
        params.append(id_roles)

    if nombre:
        condition += " AND nombre %s"
        params.append(nombre)
    
    if nivel_administracion:
        condition += " AND nivel_administracion %s"
        params.append(nivel_administracion)
    
    return query_db(sql + condition, params)