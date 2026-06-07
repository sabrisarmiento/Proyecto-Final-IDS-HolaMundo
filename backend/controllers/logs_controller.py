from database.db import query_db

def get_logs(limit=100, id_usuario=None, id_curso=None, accion=None):
    try:
        sql = """
            SELECT
                l.id_log,
                l.fecha,
                COALESCE(l.nombre_usuario, CONCAT(u.nombre, ' ', u.apellido), 'Usuario eliminado') AS usuario,
                l.id_curso,
                m.nombre  AS materia,
                c.catedra,
                l.accion,
                l.descripcion
            FROM logs_sistema l
            LEFT JOIN usuarios u ON l.id_usuario = u.id_usuario
            LEFT JOIN cursos   c ON l.id_curso   = c.id_curso
            LEFT JOIN materias m ON c.id_materia  = m.id_materia
            WHERE 1=1
        """
        params = []

        if id_usuario:
            sql += " AND l.id_usuario = %s"
            params.append(int(id_usuario))
        if id_curso:
            sql += " AND l.id_curso = %s"
            params.append(int(id_curso))
        if accion:
            sql += " AND l.accion = %s"
            params.append(accion)

        sql += " ORDER BY l.fecha DESC LIMIT %s"
        params.append(int(limit))

        result = query_db(sql, params)
        return {"ok": True, "data": result}
    except Exception as e:
        return {"ok": False, "code": 500, "message": "Internal Server Error", "description": str(e)}