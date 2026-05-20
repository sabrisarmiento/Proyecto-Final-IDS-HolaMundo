from database.db import query_db

def get_all_assistants():
	query = "SELECT * FROM ayudantes;"
	params = ()

	result = query_db(query, params)
	return result

def get_assistant_by_id(id):
	query = "SELECT * FROM ayudantes WHERE id = %s;"
	params = (id,)

	result = query_db(query, params)
	return result