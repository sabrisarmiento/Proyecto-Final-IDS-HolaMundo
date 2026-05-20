from database.db import query_db

def get_all_professors():
    query = "SELECT * FROM profesores"
    params = ()

    result = query_db(query, params)
    return result