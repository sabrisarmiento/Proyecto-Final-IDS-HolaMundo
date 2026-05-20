from database.db import query_db, modify_db

# GET GENERAL
def get_all_teams():
    query = """SELECT * FROM equipos;"""
    params = ()
    result = query_db(query, params)
    return result

# GET POR ID
def get_team_by_id(id):
    query = """SELECT * FROM equipos WHERE id_equipo = %s;"""
    params = (id,)
    result = query_db(query, params)
    return result

# GET POR INTEGRANTES
def get_team_by_members(id_usuario):
    query = """
        SELECT
            e.id_equipo,
            e.nombre_equipo
        FROM equipos e
        JOIN alumnos a
            ON e.id_equipo = a.id_equipo
        WHERE a.id_usuario = %s;
    """
    params = (id_usuario,)
    result = query_db(query, params)
    return result

# POST
def create_team(nombre_equipo):
    query = """INSERT INTO equipos(nombre_equipo) VALUES (%s);"""
    params = (nombre_equipo,)
    result = modify_db(query, params)
    return result

# PATCH
def update_team(id, nombre_equipo):
    query = """UPDATE equipos SET nombre_equipo = %s WHERE id_equipo = %s;"""
    params = (nombre_equipo, id)
    result = modify_db(query, params)
    return result

# DELETE
def delete_team(id):
    query = """DELETE FROM equipos WHERE id_equipo = %s;"""
    params = (id,)
    result = modify_db(query, params)
    return result