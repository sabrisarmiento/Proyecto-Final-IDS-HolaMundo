from database.db import query_db

def user_belongs_to_course(id_user, id_course):
    sql = """
        SELECT id_curso
        FROM cursos
        WHERE id_curso = %s
        AND id_profesor = %s

        UNION

        SELECT id_curso
        FROM curso_ayudantes
        WHERE id_curso = %s
        AND id_usuario = %s
    """

    result = query_db(sql, (id_course, id_user, id_course, id_user))

    belongs = False

    if len(result) > 0:
        belongs = True

    return belongs
