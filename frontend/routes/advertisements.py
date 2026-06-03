from flask import Blueprint, render_template, session
#from services.advertisement_frontend_service import AdvertisementFrontendService
from services.course_frontend_service import CourseFrontendService
#from services.slack_advertisement_frontend_service import SlackAdvertisementFrontendService
from services.advertisement_frontend_service import get_all_combined_advertisements

advertisements_bp = Blueprint('advertisements', __name__)

@advertisements_bp.route('/avisos')
def public_advertisements():

    id_curso = session.get("selected_course")

    #avisos = AdvertisementFrontendService.get_all(id_curso)
    avisos = get_all_combined_advertisements(id_curso)

    cursos = CourseFrontendService.get_all() #hay que cambiar este una vez q saquen la clase

    return render_template(
        "advertisements.html",
        avisos=avisos,
        cursos=cursos,
        selected_course=id_curso,
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