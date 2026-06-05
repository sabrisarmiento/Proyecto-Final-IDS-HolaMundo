from flask import Blueprint, render_template, request
#from services.advertisement_frontend_service import AdvertisementFrontendService
#from services.slack_advertisement_frontend_service import SlackAdvertisementFrontendService
from services.subjects_service import get_subjects
from services.advertisments_service import get_advertisements_by_subject

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