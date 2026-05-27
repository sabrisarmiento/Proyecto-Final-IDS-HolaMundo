CREATE DATABASE IF NOT EXISTS DB_ProyectoFinal_IDS;
USE DB_ProyectoFinal_IDS;

-- roles --
CREATE TABLE roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    nivel_administracion INT NOT NULL
);

-- cursos --
CREATE TABLE cursos (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cuatrimestre VARCHAR(20) NOT NULL,
    anio INT NOT NULL
);

-- tipos_evaluacion --
CREATE TABLE tipos_evaluacion (
    id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT
);

-- usuarios --
CREATE TABLE usuarios (
    id_usuario int AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(255) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

-- alumnos --
CREATE TABLE alumnos (
    id_alumno INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    padron INT UNIQUE NOT NULL,
    correo VARCHAR(255) NOT NULL,
    estado_alumno BOOLEAN DEFAULT FALSE,
    id_curso INT NOT NULL,
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
);

-- equipos --
CREATE TABLE equipos (
    id_equipo INT AUTO_INCREMENT PRIMARY KEY,
    nombre_equipo VARCHAR(20) NOT NULL,
    id_curso INT NOT NULL,
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
);

-- clases --
CREATE TABLE clases (
    id_clase INT AUTO_INCREMENT PRIMARY KEY,
    fecha VARCHAR(10) NOT NULL,
    temas TEXT,
    semana INT NOT NULL,
    tipo VARCHAR(50),
    modalidad VARCHAR(50)
    id_curso INT NOT NULL,
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso) ON DELETE CASCADE
);

-- materiales --
CREATE TABLE materiales (
    id_material INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    url_externo VARCHAR(500) NOT NULL,
    id_curso INT NOT NULL,
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso) ON DELETE CASCADE
);

-- equipo_alumno -- tabla intermedia
CREATE TABLE equipo_alumno (
    id_equipo INT NOT NULL,
    id_alumno INT NOT NULL,
    PRIMARY KEY (id_equipo, id_alumno),
    FOREIGN KEY (id_equipo) REFERENCES equipos(id_equipo) ON DELETE CASCADE,
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id_alumno) ON DELETE CASCADE
);

-- asistencia --
CREATE TABLE asistencia (
    id_asistencia INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno INT NOT NULL,
    id_clase INT NOT NULL,
    presente BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id_alumno),
    FOREIGN KEY (id_clase) REFERENCES clases(id_clase) 
);

-- aviso --
CREATE TABLE avisos (
    id_aviso INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    mensaje TEXT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- evaluaciones --
CREATE TABLE evaluaciones (
    id_evaluacion INT AUTO_INCREMENT PRIMARY KEY,
    id_tipo INT NOT NULL,
    id_usuario INT NOT NULL,
    fecha DATE,
    asociacion ENUM('Individual', 'Equipo') NOT NULL,
    FOREIGN KEY (id_tipo) REFERENCES tipos_evaluacion(id_tipo),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- notas --
CREATE TABLE notas (
    id_nota INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno INT,
    id_evaluacion INT NOT NULL,
    id_equipo INT,
    nota DECIMAL(4, 2) NOT NULL,
    id_corrector INT NOT NULL,
    FOREIGN KEY (id_evaluacion) REFERENCES evaluaciones(id_evaluacion),
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id_alumno),
    FOREIGN KEY (id_equipo) REFERENCES equipos(id_equipo),
    FOREIGN KEY (id_corrector) REFERENCES usuarios(id_usuario)
);

CREATE TABLE calendario (
    id_evento INT AUTO_INCREMENT PRIMARY KEY, 
    titulo VARCHAR(100) NOT NULL,
    tipo_clase VARCHAR(50) NOT NULL,
    descripcion TEXT,
    modalidad VARCHAR(100),
    hipervinculo VARCHAR(255),
    fecha_evento DATETIME NOT NULL,
    id_profesor INT NOT NULL,
    FOREIGN KEY (id_profesor) REFERENCES usuarios (id_usuario)
);

INSERT INTO ROLES (nombre, nivel_administracion) VALUES ('Profesor', 1);

INSERT INTO USUARIOS (nombre, apellido, correo, contraseña, id_rol)
VALUES ('Bruno', 'Profe', 'bruno@fiuba.com', '123456', 1);

SELECT * FROM usuarios;
SELECT * FROM roles;