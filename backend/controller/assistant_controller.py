from database.db import query_db

def get_all_assistants():
	try:
		query = "SELECT * FROM ayudantes;"
		result = query_db(query, ())
		return {
			"ok": True,
			"data": result
		}
	except Exception as e:
		return {
			"ok": False,
			"code": 500,
			"message": "Internal Server Error",
			"description": str(e)
		}


def get_assistant_by_id(id):
	try:
		query = "SELECT * FROM ayudantes WHERE id_usuario = %s"
		params = (id,)
		result = query_db(query, params)
		return {
			"ok": True,
			"data": result[0] if result else None
		}
	except Exception as error:
		return {
			"ok": False,
			"code": 500,
			"message": "Internal Server Error",
			"description": str(error)
		}