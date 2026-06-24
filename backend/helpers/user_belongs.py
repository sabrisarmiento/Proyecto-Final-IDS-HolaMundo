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
    return user_belongs_to_course(user.get("id_usuario"), id_course)


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


def user_can_manage_equipo(id_equipo, user):
    if (user.get("nivel") or 0) >= NIVEL_SUPERADMIN:
        return True
    row = query_db("SELECT id_curso FROM equipos WHERE id_equipo = %s", (id_equipo,))
    return bool(row) and user_can_manage_course(row[0]["id_curso"], user)


def user_can_manage_evaluacion(id_evaluacion, user):
    if (user.get("nivel") or 0) >= NIVEL_SUPERADMIN:
        return True
    row = query_db("SELECT id_curso FROM evaluaciones WHERE id_evaluacion = %s", (id_evaluacion,))
    return bool(row) and user_can_manage_course(row[0]["id_curso"], user)


def user_can_manage_nota(id_nota, user):
    if (user.get("nivel") or 0) >= NIVEL_SUPERADMIN:
        return True
    row = query_db(
        "SELECT e.id_curso FROM notas n JOIN evaluaciones e ON n.id_evaluacion = e.id_evaluacion WHERE n.id_nota = %s",
        (id_nota,),
    )
    return bool(row) and user_can_manage_course(row[0]["id_curso"], user)


def user_can_manage_material(id_material, user):
    if (user.get("nivel") or 0) >= NIVEL_SUPERADMIN:
        return True
    row = query_db("SELECT id_curso FROM materiales WHERE id_material = %s", (id_material,))
    return bool(row) and user_can_manage_course(row[0]["id_curso"], user)
