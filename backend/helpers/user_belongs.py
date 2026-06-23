from database.db import query_db
from helpers.constants import NIVEL_SUPERADMIN

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


def user_can_manage_course(id_course, user):
    if (user.get("nivel") or 0) >= NIVEL_SUPERADMIN:
        return True
    course = query_db("SELECT id_profesor FROM cursos WHERE id_curso = %s", (id_course,))
    return bool(course) and course[0].get("id_profesor") == user.get("id_usuario")
