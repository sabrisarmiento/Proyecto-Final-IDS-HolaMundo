from werkzeug.security import generate_password_hash
from database.db import modify_db

def crear_usuario_ejemplo():
    nombre = "Profesor"
    apellido = "Ejemplo"
    correo = "profesor@ejemplo.com"
    password = "Profesor123!"
    id_rol = 2 

    password_hash = generate_password_hash(password)

    query = """
        INSERT INTO usuarios (nombre, apellido, correo, contraseña, id_rol)
        VALUES (%s, %s, %s, %s, %s)
    """

    params = (
        nombre,
        apellido,
        correo,
        password_hash,
        id_rol
    )

    modify_db(query, params)

    print("Usuario creado correctamente")
    print("Correo:", correo)
    print("Contraseña:", password)

crear_usuario_ejemplo()