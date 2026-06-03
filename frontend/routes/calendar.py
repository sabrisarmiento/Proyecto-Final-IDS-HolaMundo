from flask import Blueprint, render_template, session, request
from services.subjects_service import get_subjects, get_subject_by_id
from services.calendar_frontend_service import CalendarFrontendService
from services.course_frontend_service import CourseFrontendService
from services.courses_service import get_courses

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/cronograma', methods=['GET'])
def calendar():
    id_subject = request.args.get("subject")
    selected_subject = int(id_subject) if id_subject else None

    schedule = {}
    cursos = []
    cursos_by_subject = []
    subject = {}

    if selected_subject:
        cursos = get_courses()
        print("CURSOS:", cursos)

        subject = get_subject_by_id(selected_subject).get("subject", {})

        cursos_by_subject = [c for c in cursos if c.get("materia") == subject.get("nombre")]

        for curso in cursos_by_subject:
            clases_api = CalendarFrontendService.get_all(curso["id_curso"])
            for clase in clases_api:
                week_num = clase.get('semana')
                if week_num is not None:
                    if week_num not in schedule:
                        schedule[week_num] = []
                    schedule[week_num].append(clase)

    sorted_schedule = [
        {"week": w, "classes": schedule[w]}
        for w in sorted(schedule.keys())
    ]

    try:
        subjects = get_subjects()
    except Exception as e:
        print(f"Error al obtener materias: {e}")
        subjects = []

    return render_template(
        'calendar.html',
        schedule=sorted_schedule,
        cursos=cursos_by_subject,
        subject=subject,
        subjects=subjects,
        selected_subject=selected_subject,
        active_page='calendar'
    )

    # id_curso = session.get("selected_course")

    # clases_api = CalendarFrontendService.get_all(id_curso)

    # schedule = {}

    # for clase in clases_api:
    #     week_num = clase.get('semana')

    #     if week_num is not None:

    #         if week_num not in schedule:
    #             schedule[week_num] = []

    #         schedule[week_num].append(clase)

    # sorted_schedule = [
    #     {"week": w, "classes": schedule[w]}
    #     for w in sorted(schedule.keys())
    # ]

    # cursos = CourseFrontendService.get_all()

    # return render_template(
    #     'calendar.html',
    #     schedule=sorted_schedule,
    #     cursos=cursos,
    #     selected_course=id_curso,
    #     active_page='calendar'
    # )
