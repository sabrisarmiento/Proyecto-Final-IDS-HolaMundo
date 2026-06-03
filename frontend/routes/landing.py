from flask import Blueprint, render_template, session
from services.course_frontend_service import CourseFrontendService
import requests

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/', methods=["GET"])
def landing():
    print("SESION INICIADA", session.get('user'))
    print("TODO SESSION", session)

    id_curso = session.get("selected_course")

    # Avisos
    if id_curso:
        try:
            response = requests.get("http://127.0.0.1:5000/advertisements", params={"id_curso": id_curso})
            data = response.json()
            advertisements = data.get("advertisements") or []
            advertisements = advertisements[-3:][::-1]
        except Exception as e:
            print("ERROR AVISOS:", e)
            advertisements = []
    else:
        advertisements = []

    # Clases
    if id_curso:
        try:
            response = requests.get("http://127.0.0.1:5000/clases", params={"id_curso": id_curso})
            data = response.json()
            clases = data.get("classes", [])
        except Exception as e:
            print("ERROR CLASES:", e)
            clases = []
    else:
        clases = []

    # Curso seleccionado
    if id_curso:
        try:
            curso = CourseFrontendService.get_by_id(id_curso)
        except Exception as e:
            print("ERROR CURSO:", e)
            curso = {}
    else:
        curso = {}

    try:
        cursos = CourseFrontendService.get_all()
    except Exception as e:
        print("ERROR CURSOS:", e)
        cursos = []

    return render_template(
        "index.html",
        avisos=advertisements,
        clases=clases,
        curso=curso,
        cursos=cursos,
        active_page="landing",
        selected_course=id_curso
    )