from flask import Blueprint, render_template, session
from services.advertisement_frontend_service import AdvertisementFrontendService
from services.course_frontend_service import CourseFrontendService

advertisements_bp = Blueprint('advertisements', __name__)

@advertisements_bp.route('/avisos')
def public_advertisements():

    id_curso = session.get("selected_course")

    avisos = AdvertisementFrontendService.get_all(id_curso)

    cursos = CourseFrontendService.get_all()

    return render_template(
        "advertisements.html",
        avisos=avisos,
        cursos=cursos,
        selected_course=id_curso,
        active_page="advertisements"
    )