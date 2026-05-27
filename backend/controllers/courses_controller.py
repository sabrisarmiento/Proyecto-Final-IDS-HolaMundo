from database.db import query_db

def get_all_courses():
  try:
    sql = "SELECT * FROM cursos"
    condition = " WHERE 1=1"

    params = []

    result = query_db(sql + condition, params)
    return {
      "ok": True,
      "data": result
    }
  
  except Exception as e:
    return {
      "ok": False,
      "code": 500,
      "message": "Internal Server Error",
      "data": str(e)
    }