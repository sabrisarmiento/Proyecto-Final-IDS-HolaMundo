--roles--
CREATE TABLE roles {
    id_roles INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    nivel_administracion INT NOT NULL
}
--aviso--
CREATE TABLE avisos (
    id_aviso INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    mensaje TEXT NOT NULL,
    fecha DATE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
)
--usuarios--
create table usuarios (
    id_usuario int auto_increment PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL,
    apellido_usuario VARCHAR(100) NOT NULL,
    correo_usuario VARCHAR(255) NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT ,
    id_rol INT,
    FOREIGN KEY (id_rol) REFERENCES roles (id_rol)
)
