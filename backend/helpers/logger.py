from database.db import modify_db

def log_action(accion: str, descripcion: str, id_usuario=None, nombre_usuario=None, id_curso=None):
    """
    Registra una acción en logs_sistema.
    Fire-and-forget: si falla no interrumpe el flujo principal.
    """
    try:
        modify_db(
            """
            INSERT INTO logs_sistema (id_usuario, nombre_usuario, id_curso, accion, descripcion)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (id_usuario, nombre_usuario, id_curso, accion, descripcion)
        )
    except Exception as e:
        print(f"[LOGGER ERROR] {e}")