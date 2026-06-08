from database.db import query_db
from datetime import datetime


def get_general_dashboard():
    try:
        total_usuarios = query_db("SELECT COUNT(*) AS total FROM usuarios")[0]["total"]
        anio_actual = datetime.now().year
        mes_actual = datetime.now().month
        cuatrimestre_actual = 1 if mes_actual <= 7 else 2
        cursos_activos = query_db(
            "SELECT COUNT(*) AS total FROM cursos WHERE anio = %s AND cuatrimestre = %s",
            (anio_actual, cuatrimestre_actual)
        )[0]["total"]

        total_alumnos = query_db("SELECT COUNT(*) AS total FROM alumnos")[0]["total"]

        usuarios = query_db(
            """
            SELECT u.id_usuario, u.nombre, u.apellido, u.correo, u.creado,
                   r.nombre AS rol_nombre, r.nivel_administracion, r.id_rol
            FROM usuarios u
            LEFT JOIN roles r ON u.id_rol = r.id_rol
            ORDER BY r.nivel_administracion DESC, u.apellido, u.nombre
            """
        )

        roles = query_db("SELECT id_rol, nombre, nivel_administracion FROM roles ORDER BY nivel_administracion DESC")

        rendimiento_historico = query_db(
            """
            SELECT c.anio, ROUND(AVG(n.nota), 2) AS promedio_notas
            FROM notas n
            JOIN evaluaciones e ON n.id_evaluacion = e.id_evaluacion
            JOIN cursos c ON e.id_curso = c.id_curso
            GROUP BY c.anio
            ORDER BY c.anio ASC
            """
        )

        cursos_stats = query_db(
            """
            SELECT c.id_curso,
                   m.nombre AS materia,
                   c.catedra,
                   c.anio,
                   c.cuatrimestre,
                   COUNT(a.id_alumno) AS total_alumnos,
                   SUM(CASE WHEN a.estado_alumno = 1 THEN 1 ELSE 0 END) AS activos,
                   SUM(CASE WHEN a.estado_alumno = 0 THEN 1 ELSE 0 END) AS abandono
            FROM cursos c
            JOIN materias m ON c.id_materia = m.id_materia
            LEFT JOIN alumnos a ON c.id_curso = a.id_curso
            WHERE c.anio = %s AND c.cuatrimestre = %s
            GROUP BY c.id_curso, m.nombre, c.catedra, c.anio, c.cuatrimestre
            ORDER BY m.nombre
            """,
            (anio_actual, cuatrimestre_actual)
        )

        return {
            "ok": True,
            "data": {
                "total_usuarios": total_usuarios,
                "cursos_activos": cursos_activos,
                "total_alumnos": total_alumnos,
                "usuarios": usuarios,
                "roles": roles,
                "rendimiento_historico": rendimiento_historico,
                "cursos_stats": cursos_stats,
                "anio_actual": anio_actual,
                "cuatrimestre_actual": cuatrimestre_actual,
            }
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }