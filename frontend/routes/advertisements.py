from flask import Blueprint, render_template, request, session, redirect, url_for
#from services.advertisement_frontend_service import AdvertisementFrontendService
#from services.slack_advertisement_frontend_service import SlackAdvertisementFrontendService
from services.subjects_service import get_subjects
from services.advertisements_service import get_advertisements_by_subject, create_advertisement

advertisements_bp = Blueprint('advertisements', __name__)

@advertisements_bp.route('/avisos')
def public_advertisements():
  avisos = []
  view = request.args.get("subject")

  if view is not None:
    try:
      avisos = get_advertisements_by_subject(int(view))
    except Exception as e:
      print(f"Error al obtener avisos para la materia {view}: {e}")
  
  subjects = get_subjects()
  
  return render_template(
    "advertisements.html",
    active_page="advertisements",
    avisos=avisos,
    subjects=subjects,
    selected_subject=int(view) if view else None
  )

@advertisements_bp.route('/cursos/<int:id_curso>/avisos/nuevo', methods=['GET', 'POST'])
def create_advertisement_front(id_curso):
  if request.method == 'POST':
    title = request.form.get("titulo")
    message = request.form.get("mensaje")
    token = session.get("token")

    if not token:
      return redirect(url_for("auth.login"))

    result = create_advertisement(id_curso, title, message, token)

    if result["ok"]:
      return redirect(url_for("advertisements.public_advertisements"))

    return render_template(
      "create_advertisement.html",
      id_curso=id_curso,
      error="No se pudo crear el aviso"
    )

  return render_template(
    "create_advertisement.html",
    id_curso=id_curso
  )
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