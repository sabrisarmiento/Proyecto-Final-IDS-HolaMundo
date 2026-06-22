# Levantar el proyecto con Docker

Guía para correr **Panel FIUBA** completo (frontend + backend + base de datos) en contenedores, sin instalar Python ni MySQL a mano.

Con un solo comando se levantan **3 servicios**:

| Servicio | Qué es | Puerto |
|---|---|---|
| `db` | MySQL 8.4 (crea la base y carga el schema + datos de prueba solo) | 3306 |
| `backend` | API Flask | 5000 |
| `frontend` | La web Flask | 5001 |

---

## 1. Requisitos

- **Docker Desktop** instalado y **abierto** (esperá a que diga *Engine running* / el ballenita esté en verde).
  - Descarga: https://www.docker.com/products/docker-desktop/
- **Git**.

> No hace falta instalar Python ni MySQL: va todo adentro de Docker.

---

## 2. Pasos

### a) Clonar el repo
```bash
git clone https://github.com/sabrisarmiento/Proyecto-Final-IDS-HolaMundo.git
cd Proyecto-Final-IDS-HolaMundo
```

### b) Pararse en la branch con Docker
```bash
git checkout feat/dockerize
```
> Cuando esta branch se mergee, los archivos van a estar en `develop` y este paso no hará falta.

### c) Crear el archivo `.env`
Copiá la plantilla:
```bash
cp backend/.env.example backend/.env
```
> En PowerShell o cmd (Windows): `copy backend\.env.example backend\.env`

Los valores por defecto ya funcionan. **Solo si querés que mande mails de asistencia**, abrí `backend/.env` y completá:
- `EMAIL_USER`: el mail de la cuenta de Gmail que envía.
- `EMAIL_PASS`: un **App Password de 16 caracteres** (no la contraseña normal). Se genera en la cuenta de Google → Seguridad → Verificación en 2 pasos → Contraseñas de aplicaciones.

Sin esto la app anda igual, solo que no envía correos.

### d) Levantar todo
```bash
docker compose up --build
```
La **primera vez tarda unos minutos** (baja la imagen de MySQL, arma las imágenes y carga la base). Cuando veas que los servicios quedaron arriba, ya está.

> Tip: agregá `-d` al final (`docker compose up --build -d`) para que corra en segundo plano y te devuelva la terminal.

### e) Entrar
- **Web: http://localhost:5001**
- API: http://localhost:5000
- Usuario de prueba: **profe@fiuba.com** / **Profesor123!**

---

## 3. Comandos útiles

| Para... | Comando |
|---|---|
| Frenar (sin borrar la base) | `docker compose down` |
| Frenar y **borrar la base** (recarga los datos de prueba al volver) | `docker compose down -v` |
| Ver los logs en vivo | `docker compose logs -f` |
| Ver logs de un servicio | `docker compose logs -f backend` |
| Reconstruir tras cambiar código | `docker compose up --build` |
| Ver qué contenedores están arriba | `docker compose ps` |

> Los datos se guardan en un volumen (`db_data`), así que con `down` y después `up` **no se pierde nada**. Solo `down -v` borra la base y la vuelve a cargar desde el seed.

---

## 4. Si algo falla

- **`port is already allocated` (3306, 5000 o 5001):** ya tenés algo ocupando ese puerto (por ejemplo un MySQL local). Cerralo y volvé a probar.
- **`Cannot connect to the Docker daemon`:** Docker Desktop no está corriendo. Abrilo, esperá a que levante el motor y reintentá.
- **El backend tira error de conexión apenas levanta:** la base tarda unos segundos en estar lista; el backend la espera, pero si abriste la web muy rápido, recargá en unos segundos.
