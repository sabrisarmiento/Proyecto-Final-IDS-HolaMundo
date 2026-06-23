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


def user_can_manage_clase(id_clase, user):
    if (user.get("nivel") or 0) >= NIVEL_SUPERADMIN:
        return True
    row = query_db("SELECT id_curso FROM clases WHERE id_clase = %s", (id_clase,))
    return bool(row) and user_can_manage_course(row[0]["id_curso"], user)


def user_can_manage_alumno(id_alumno, user):
    if (user.get("nivel") or 0) >= NIVEL_SUPERADMIN:
        return True
    row = query_db("SELECT id_curso FROM alumnos WHERE id_alumno = %s", (id_alumno,))
    return bool(row) and user_can_manage_course(row[0]["id_curso"], user)
