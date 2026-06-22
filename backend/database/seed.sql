-- Datos de prueba mínimos para Panel FIUBA
-- Login: admin@fiuba.com / 1234

SET NAMES utf8mb4;
USE DB_ProyectoFinal_IDS;

INSERT INTO roles (id_rol, nombre, nivel_administracion) VALUES
  (1, 'Superadmin', 3),
  (2, 'Profesor', 2),
  (3, 'Ayudante', 1);

INSERT INTO usuarios (id_usuario, nombre, apellido, correo, contraseña, id_rol) VALUES
  (1, 'Superadmin', 'Admin', 'admin@fiuba.com', 'scrypt:32768:8:1$Bvlk5x0NHzhgDqrl$4aa684d565b617787a84869c5db83bc6f6f3aee3f2e84785445a8fc451def20ab0137ad8512d34fdf2c5a6c06d0cfcd38f574f4cf591bbc190b21dfcb7ec3d2f', 1);
