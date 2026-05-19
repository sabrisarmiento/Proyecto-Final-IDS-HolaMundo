--roles--
CREATE TABLE roles {
    id_roles INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    nivel_administracion INT NOT NULL
}

--clases--
CREATE TABLE clases(
    id_clase INT PRIMARY KEY,
    fecha DATE,
    temas VARCHAR(255)
)

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

--alumnos--
CREATE TABLE IF NOT EXISTS alumnos (
    id_usuario INT PRIMARY KEY,
    padron INT UNIQUE NOT NULL,
    estado_alumno ENUM('Activo', 'Baja solicitada', 'Abandono') NOT NULL,
    id_equipo INT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario),
    FOREIGN KEY (id_equipo) REFERENCES equipos (id_equipo)
);

--ayudantes--
CREATE TABLE ayudantes (
    id_usuario INT PRIMARY KEY,
    id_equipo INT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_equipo) REFERENCES equipos(id_equipo)
)

--profesores--
create table profesores (
    id_usuario INT PRIMARY KEY
    id_equipo INT
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
    FOREIGN KEY (id_equipo) REFERENCES equipo (id_equipo)
)

--evaluaciones--
CREATE TABLE evaluaciones (
    id_evaluacion INT PRIMARY KEY,
    id_tipo INT,
    id_profesor INT,
    id_equipo INT,
    fecha DATE,
    FOREIGN KEY (id_tipo) REFERENCES tipos_evaluacion(id_tipo),
    FOREIGN KEY (id_profesor) REFERENCES profesores(id_usuario),
    FOREIGN KEY (id_equipo) REFERENCES equipos(id_equipo)
);

--notas--
CREATE TABLE notas (
    id_nota INT PRIMARY KEY,
    id_alumno INT,
    id_evaluacion INT,
    nota DECIMAL(4, 2),
    FOREIGN KEY (id_alumno) REFERENCES alumnos (id_usuario),
    FOREIGN KEY (id_evaluacion) REFERENCES evaluaciones (id_evaluacion)
);