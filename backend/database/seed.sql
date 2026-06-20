-- Datos de prueba para Panel FIUBA
-- Cargar DESPUES del schema (database_finalIDS.sql).
-- Login: profe@fiuba.com / Profesor123!

USE db_proyectofinal_ids;

INSERT INTO roles (id_rol, nombre, nivel_administracion) VALUES
  (1, 'Ayudante', 1),
  (2, 'Profesor', 2),
  (3, 'Superadmin', 3);

INSERT INTO usuarios (id_usuario, nombre, apellido, correo, contraseña, id_rol) VALUES
  (1, 'Bruno', 'Lanzillotta', 'profe@fiuba.com', 'scrypt:32768:8:1$g5TgqgO3iKklNVAH$27c8521a3d6e8718cc4e7104de293ead522dfa36b6477437dc8e801863cf2ed932d04cff76e52d69dba83fd9681258f11a92d68cb2992ab0e97430eb7acf72d0', 2);

INSERT INTO materias (id_materia, nombre, codigo, descripcion) VALUES
  (1, 'IDS', '7507', 'Introduccion al Desarrollo de Software');

INSERT INTO cursos (id_curso, id_materia, catedra, id_profesor, cuatrimestre, anio) VALUES
  (1, 1, 'Lanzillotta', 1, '1C', 2026);

INSERT INTO tipos_evaluacion (id_tipo, nombre, descripcion) VALUES
  (1, 'Parcial', 'Examen parcial'),
  (2, 'TP', 'Trabajo practico');

INSERT INTO clases (id_clase, fecha, temas, semana, tipo, modalidad, id_curso) VALUES
  (1, '2026-06-02', 'Introduccion y Git',    1, 'Teorica',  'Presencial', 1),
  (2, '2026-06-09', 'Docker y contenedores', 2, 'Teorica',  'Virtual',    1),
  (3, '2026-06-16', 'Kubernetes',            3, 'Practica', 'Presencial', 1),
  (4, '2026-06-23', 'CI/CD y despliegue',    4, 'Practica', 'Virtual',    1);

INSERT INTO alumnos (id_alumno, nombre, apellido, padron, correo, estado_alumno, id_curso) VALUES
  (1, 'Ana',   'Test',   100001, 'ana@test.com',   1, 1),
  (2, 'Beto',  'Prueba', 100002, 'beto@test.com',  1, 1),
  (3, 'Carla', 'Gomez',  100003, 'carla@test.com', 1, 1),
  (4, 'Diego', 'Lopez',  100004, 'diego@test.com', 1, 1);

INSERT INTO equipos (id_equipo, nombre_equipo, id_curso) VALUES
  (1, 'Equipo A', 1);

INSERT INTO equipo_alumno (id_equipo, id_alumno) VALUES
  (1, 1),
  (1, 2);

INSERT INTO evaluaciones (id_evaluacion, id_tipo, id_curso, id_usuario, fecha, asociacion) VALUES
  (1, 1, 1, 1, '2026-06-10', 'Individual'),
  (2, 2, 1, 1, '2026-06-17', 'Individual');

INSERT INTO notas (id_nota, id_alumno, id_evaluacion, nota, corrector_nombre) VALUES
  (1, 1, 1, 8.00, 'Bruno'),
  (2, 2, 1, 5.00, 'Bruno'),
  (3, 3, 1, 9.00, 'Bruno'),
  (4, 1, 2, 7.50, 'Bruno'),
  (5, 2, 2, 4.00, 'Bruno');

INSERT INTO asistencia (id_alumno, id_clase, presente) VALUES
  (1, 1, 1), (2, 1, 1), (3, 1, 1),
  (1, 2, 1), (3, 2, 1),
  (1, 3, 1), (2, 3, 1), (4, 3, 1);

INSERT INTO materiales (id_material, titulo, descripcion, url_externo, id_curso, id_clase) VALUES
  (1, 'Apunte Docker',   'Slides de la clase de contenedores', 'https://ejemplo.com/docker.pdf', 1, 2),
  (2, 'Guia Kubernetes', 'Comandos basicos de kubectl',        'https://ejemplo.com/k8s.pdf',    1, 3);

INSERT INTO configuracion_promocion (id_curso, es_promocionable, id_evaluacion, cuenta_para_promocion, nota_minima) VALUES
  (1, TRUE, 1, TRUE, 4.00),
  (1, TRUE, 2, TRUE, 4.00);

INSERT INTO curso_promocion_config (id_curso, es_promocionable, porcentaje_asistencia, cuenta_asistencia) VALUES
  (1, TRUE, 75.00, TRUE);
