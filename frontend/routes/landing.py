from flask import Blueprint, render_template, session, request
from services.subjects_service import get_subjects, get_subject_by_id, get_topics_by_subject_id
from services.courses_service import get_courses
import requests

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/', methods=["GET"])
def landing():
    print("DATOS DE LA SESSION de Flask")
    print(session)

    id_subject = request.args.get("subject")
    selected_subject = int(id_subject) if id_subject else None

    advertisements = []
    clases = []
    cursos = []
    subject = {}
    temas = []

    if id_subject:
        try:
            all_courses = get_courses()
            resp = get_subject_by_id(id_subject)
            subject = resp.get("subject", {})   # 👈 desanidás acá
            print("SUBJECT:", subject)

            courses_by_subject = [c for c in all_courses if c.get("materia") == subject.get("nombre")]
            cursos = courses_by_subject

            for c in courses_by_subject:
                id_course = c.get("id_curso")

                try:
                    resp_adv = requests.get("http://127.0.0.1:5000/advertisements", params={"id_curso": id_course}).json()
                    advertisements.extend(resp_adv.get("advertisements", []))
                except Exception as e:
                    print(f"Error en obtener anuncion de los cursos: {e}")

                try:
                    resp_clases = requests.get("http://127.0.0.1:5000/classes", params={"id_curso": id_course}).json()
                    clases.extend(resp_clases.get("classes", []))
                except Exception as e:
                    print(f"Error en obtener clases de los cursos: {e}")
        except Exception as e:
            print(f"Error en obtener cursos por materia: {e}")
        try:
            subject = get_subject_by_id(id_subject)
        except Exception as e:
            print(f"Error en obtener materia: {e}")
            subject = {}

        try:
            temas = get_topics_by_subject_id(id_subject)
        except Exception as e:
            print(f"Error en obtener temas de la materia: {e}")
            temas = []

    try:
        subjects = get_subjects()
    except Exception as e:
        print(f"Error en obtener materia: {e}")
        subjects = []

    print("CURSOS:" , cursos)

    return render_template(
        "index.html",
        avisos=advertisements,
        clases=clases,
        subject=subject,
        subjects=subjects,
        cursos=cursos,
        temas=temas,
        active_page="landing",
        selected_subject=selected_subject
    )