from database.db import query_db
from datetime import datetime


def get_general_dashboard():
    try:
        anio_actual = datetime.now().year
        mes_actual  = datetime.now().month
        cuatrimestre_actual = 1 if mes_actual <= 7 else 2

        total_usuarios = query_db("SELECT COUNT(*) AS total FROM usuarios")[0]["total"]

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

        roles = query_db(
            "SELECT id_rol, nombre, nivel_administracion FROM roles ORDER BY nivel_administracion DESC"
        )

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

        logs_recientes = query_db(
            """
            SELECT
                l.id_log,
                l.fecha,
                COALESCE(l.nombre_usuario, CONCAT(u.nombre, ' ', u.apellido), 'Usuario eliminado') AS usuario,
                l.accion,
                l.descripcion,
                m.nombre  AS materia,
                c.catedra
            FROM logs_sistema l
            LEFT JOIN usuarios u ON l.id_usuario = u.id_usuario
            LEFT JOIN cursos   c ON l.id_curso   = c.id_curso
            LEFT JOIN materias m ON c.id_materia  = m.id_materia
            ORDER BY l.fecha DESC
            LIMIT 50
            """
        )

        return {
            "ok": True,
            "data": {
                "total_usuarios":        total_usuarios,
                "cursos_activos":        cursos_activos,
                "total_alumnos":         total_alumnos,
                "usuarios":              usuarios,
                "roles":                 roles,
                "rendimiento_historico": rendimiento_historico,
                "cursos_stats":          cursos_stats,
                "logs_recientes":        logs_recientes,
                "anio_actual":           anio_actual,
                "cuatrimestre_actual":   cuatrimestre_actual,
            }
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }