from flask import Blueprint, render_template, session, request
#from services.advertisement_frontend_service import AdvertisementFrontendService
from services.course_frontend_service import CourseFrontendService
#from services.slack_advertisement_frontend_service import SlackAdvertisementFrontendService
from services.advertisement_frontend_service import get_all_combined_advertisements
from services.courses_service import get_courses
from services.subjects_service import get_subject_by_id, get_subjects

advertisements_bp = Blueprint('advertisements', __name__)

@advertisements_bp.route('/avisos')
def public_advertisements():
    id_subject = request.args.get("subject")
    avisos = []
    cursos = []
    subjects = []

    if id_subject:
        id_subject = int(id_subject)
        cursos = get_courses()
        subject = get_subject_by_id(id_subject).get("subject", {})
        cursos_by_subject = [c for c in cursos if c.get("materia") == subject.get("nombre")]

        for curso in cursos_by_subject:
            avisos.extend(get_all_combined_advertisements(curso["id_curso"]))

    try:
        subjects = get_subjects()
    except Exception as e:
        print(f"Error al obtener materias: {e}")

    subject = get_subject_by_id(id_subject).get("subject", {}) if id_subject else {}

    return render_template(
        "advertisements.html",
        avisos=avisos,
        cursos=cursos_by_subject,
        subject=subject,
        subjects=subjects,
        selected_subject=id_subject,
        active_page="advertisements"
    )


# @advertisements_bp.route('/avisos/slack')
# def slack_advertisements():

#     id_curso = session.get("selected_course", 1)

#     avisos = SlackAdvertisementFrontendService.get_all()

#     cursos = CourseFrontendService.get_all()

#     return render_template(
#         "advertisements.html",
#         avisos=avisos,
#         cursos=cursos,
#         selected_course=id_curso,
#         active_page="advertisements"
#     )