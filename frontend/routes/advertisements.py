from config import BASE_URL
from flask import Blueprint, render_template, request, session, redirect, url_for
import requests
#from services.advertisement_frontend_service import AdvertisementFrontendService
#from services.slack_advertisement_frontend_service import SlackAdvertisementFrontendService
from services.subjects_service import get_subjects
from services.advertisements_service import get_advertisements_by_subject, create_advertisement, get_advertisement_by_id, update_advertisement, delete_advertisement
from services.courses_service import get_courses

advertisements_bp = Blueprint('advertisements', __name__)

#@advertisements_bp.route('/avisos')
#def public_advertisements():
#  avisos = []
#  view = request.args.get("subject")

#  if view is not None:
#    try:
#      avisos = get_advertisements_by_subject(int(view))
#    except Exception as e:
#      print(f"Error al obtener avisos para la materia {view}: {e}")
  
#  subjects = get_subjects()
  
#  return render_template(
#    "advertisements.html",
#    active_page="advertisements",
#    subjects=subjects,
#    avisos=avisos,
#    selected_subject=int(view) if view else None
#  )

@advertisements_bp.route('/cursos/<int:id_curso>/avisos/nuevo', methods=['GET', 'POST'])
def create_advertisement_front(id_curso):
  if request.method == 'POST':
    title = request.form.get("titulo")
    message = request.form.get("mensaje")
    token = session.get("token")

    if not token:
      return redirect(url_for("landing.landing") + "?error=Debes iniciar sesión")

    result = create_advertisement(id_curso, title, message, token)

    if result["ok"]:
      return redirect(url_for("courses.course_detail", course_id=id_curso) + "?tab=ads")

    return render_template(
      "create_advertisement.html",
      id_curso=id_curso,
      error="No se pudo crear el aviso"
    )

  return render_template(
    "create_advertisement.html",
    id_curso=id_curso
  )

# @advertisements_bp.route("/cursos/<int:id_curso>/slack/conectar")
# def connect_slack_front(id_curso):
#     token = session.get("token")

#     if not token:
#         return redirect(url_for("landing.landing") + "?error=Debes iniciar sesión")
    
#     response = requests.get(
#         f"{BASE_URL}/slack/install/{id_curso}",
#         headers={
#             "Authorization": f"Bearer {token}"
#         },
#         allow_redirects=False
#     )

#     if response.status_code in [301, 302]:
#         return redirect(response.headers["Location"])

#     return redirect(url_for("courses.course_detail", course_id=id_curso) + "?tab=ads")

# @advertisements_bp.route('/avisos/slack')
# def slack_advertisements():

#     id_curso = session.get("selected_course", 1)

#     avisos = SlackAdvertisementFrontendService.get_all()

#     cursos = course_get_all()

#     return render_template(
#         "advertisements.html",
#         avisos=avisos,
#         cursos=cursos,
#         selected_course=id_curso,
#         active_page="advertisements"
#     )

@advertisements_bp.route('/avisos')
def public_advertisements():
  view = request.args.get("subject")
  avisos = []
  courses = []
  subjects = get_subjects()

  if view is not None:
    try:
      avisos = get_advertisements_by_subject(int(view))
      all_courses = get_courses()

      subject = next((s for s in subjects if s["id_materia"] == int(view)), None)
      subject_name = subject.get("nombre") if subject else None

      courses = [c for c in all_courses if c.get("materia") == subject_name]

    except Exception as e:
      print(f"Error al obtener avisos para la materia {view}: {e}")

  print("courses", courses)

  return render_template(
    "advertisements.html",
    active_page="advertisements",
    selected_subject=int(view) if view else None,
    subjects=subjects,
    avisos=avisos,
    courses=courses
  )

@advertisements_bp.route("/cursos/<int:id_curso>/slack/configurar", methods=["GET", "POST"])
def configure_slack_front(id_curso):
    token = session.get("token")

    if not token:
        return redirect(url_for("landing.landing") + "?error=Debes iniciar sesión")

    if request.method == "POST":
        slack_bot_token = request.form.get("slack_bot_token")
        slack_channel_id = request.form.get("slack_channel_id")
        slack_channel_name = request.form.get("slack_channel_name")

        permite_escritura = request.form.get("permite_escritura") == "on"
        permite_lectura = request.form.get("permite_lectura") == "on"

        response = requests.post(
            f"{BASE_URL}/courses/{id_curso}/slack/config",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "slack_bot_token": slack_bot_token,
                "slack_channel_id": slack_channel_id,
                "slack_channel_name": slack_channel_name,
                "permite_escritura": permite_escritura,
                "permite_lectura": permite_lectura
            }
        )

        if response.status_code in [200, 201]:
            return redirect(url_for("courses.course_detail", course_id=id_curso) + "?tab=ads")

        return render_template(
            "configure_slack.html",
            id_curso=id_curso,
            error="No se pudo configurar Slack"
        )

    return render_template(
        "configure_slack.html",
        id_curso=id_curso
    )

@advertisements_bp.route("/cursos/<int:id_curso>/slack/desconectar", methods=["POST"])
def disconnect_slack_front(id_curso):
    token = session.get("token")

    if not token:
        return redirect(url_for("landing.landing") + "?error=Debes iniciar sesión")

    requests.delete(
        f"{BASE_URL}/courses/{id_curso}/slack/disconnect",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return redirect(url_for("courses.course_detail", course_id=id_curso) + "?tab=ads")

@advertisements_bp.route('/avisos/<int:id_aviso>/editar', methods=['GET', 'POST'])
def edit_advertisement_front(id_aviso):
  token = session.get("token")

  if not token:
    return redirect(url_for("landing.landing") + "?error=Debes iniciar sesión")

  if request.method == 'POST':
    title = request.form.get("titulo")
    message = request.form.get("mensaje")
    id_curso = request.form.get("id_curso")

    result = update_advertisement(id_aviso, title, message, token)

    if result["ok"]:
      if id_curso:
        return redirect(url_for("courses.course_detail", course_id=id_curso) + "?tab=ads")

      return redirect(url_for("advertisements.public_advertisements"))

    aviso = {
      "id_aviso": id_aviso,
      "titulo": title,
      "mensaje": message,
      "id_curso": id_curso
    }

    return render_template(
      "edit_advertisement.html",
      aviso=aviso,
      id_curso=id_curso,
      error="No se pudo editar el aviso"
    )
  id_curso = request.args.get("id_curso")

  result = get_advertisement_by_id(id_aviso, token)

  if not result["ok"]:
    return redirect(url_for("advertisements.public_advertisements") + "?error=No se pudo obtener el aviso")

  aviso = result["data"]

  if isinstance(aviso, list):
    if len(aviso) == 0:
      return redirect(url_for("advertisements.public_advertisements") + "?error=No se encontró el aviso")
    aviso = aviso[0]

  return render_template(
    "edit_advertisement.html",
    aviso=aviso,
    id_curso=id_curso
  )


@advertisements_bp.route('/avisos/<int:id_aviso>/eliminar', methods=['POST'])
def delete_advertisement_front(id_aviso):
  token = session.get("token")
  id_curso = request.form.get("id_curso")

  if not token:
    return redirect(url_for("landing.landing") + "?error=Debes iniciar sesión")

  result = delete_advertisement(id_aviso, token)

  if not result["ok"]:
    if result.get("status_code") == 403:
      return redirect(url_for("advertisements.public_advertisements") + "?error=No tenés permiso para borrar este aviso")

  if id_curso:
    return redirect(url_for("courses.course_detail", course_id=id_curso) + "?tab=ads")

  return redirect(url_for("advertisements.public_advertisements"))