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
--asistencia--
CREATE TABLE asistencia (
    id_asistencia INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    fecha DATE,
    status BOOLEAN,
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

--ayudantes--
CREATE TABLE ayudantes (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_equipo INT,
    FOREIGN KEY (id_usuario) REFERENCES (id_usuario)
    FOREIGN KEY (id_equipo) REFERENCES (id_equipo)
)

--profesores--
create table profesores (
    id_usuario INT PRIMARY KEY
    id_equipo INT
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
    FOREIGN KEY (id_equipo) REFERENCES equipo (id_equipo)
)