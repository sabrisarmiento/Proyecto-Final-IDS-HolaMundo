from config import BASE_URL
from flask import Blueprint, render_template, session, request
from services.subjects_service import get_subjects, get_subject_by_id, get_topics_by_subject_id
from services.courses_service import get_courses
import requests

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/', methods=["GET"])
def landing():
    id_subject = request.args.get("subject")
    id_curso = request.args.get("curso")
    selected_subject = int(id_subject) if id_subject else None
    selected_curso = int(id_curso) if id_curso else None

    advertisements = []
    clases = []
    cursos = []
    subject = {}
    temas = []
    docentes = []

    if id_subject:
        try:
            subject = get_subject_by_id(id_subject)
        except Exception as e:
            print(f"Error en obtener materia: {e}")
            subject = {}

        try:
            temas = get_topics_by_subject_id(id_subject)
        except Exception as e:
            print(f"Error en obtener temas de la materia: {e}")

        try:
            all_courses = get_courses()
            subject_name = subject.get("subject", {}).get("nombre") if isinstance(subject.get("subject"), dict) else None
            cursos = [c for c in all_courses if c.get("materia") == subject_name]
        except Exception as e:
            print(f"Error en obtener cursos por materia: {e}")

        if id_curso:
            curso_actual = next((c for c in cursos if c.get("id_curso") == int(id_curso)), None)
            cursos_a_mostrar = [curso_actual] if curso_actual else []

            try:
                resp_adv = requests.get(f"{BASE_URL}/advertisements", params={"id_curso": id_curso}).json()
                advertisements = resp_adv.get("advertisements", [])
            except Exception as e:
                print(f"Error en obtener avisos: {e}")

            try:
                resp_clases = requests.get(f"{BASE_URL}/classes", params={"id_curso": id_curso}).json()
                clases = resp_clases.get("classes", [])
            except Exception as e:
                print(f"Error en obtener clases: {e}")

            try:
                resp_course = requests.get(f"{BASE_URL}/courses/{id_curso}").json()
                course_detail = resp_course.get("course", {})
                seen_ids = set()

                if course_detail.get("profesor_id"):
                    docentes.append({
                        "id_usuario": course_detail["profesor_id"],
                        "nombre": course_detail["profesor_nombre"],
                        "apellido": course_detail["profesor_apellido"],
                        "rol": "Profesor Titular"
                    })
                    seen_ids.add(course_detail["profesor_id"])

                for ayudante in course_detail.get("ayudantes", []):
                    if ayudante["id_usuario"] not in seen_ids:
                        docentes.append({
                            "id_usuario": ayudante["id_usuario"],
                            "nombre": ayudante["nombre"],
                            "apellido": ayudante["apellido"],
                            "rol": "Ayudante"
                        })
                        seen_ids.add(ayudante["id_usuario"])
            except Exception as e:
                print(f"Error en obtener docentes: {e}")
        else:
            cursos_a_mostrar = cursos
    else:
        cursos_a_mostrar = []

    try:
        subjects = get_subjects()
    except Exception as e:
        print(f"Error en obtener materias: {e}")
        subjects = []

    return render_template(
        "index.html",
        avisos=advertisements,
        clases=clases,
        subject=subject,
        subjects=subjects,
        cursos=cursos_a_mostrar,
        cursos_catedra=cursos,
        temas=temas,
        docentes=docentes,
        active_page="landing",
        selected_subject=selected_subject,
        selected_curso=selected_curso
    )