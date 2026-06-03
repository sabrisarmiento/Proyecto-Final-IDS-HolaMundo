from flask import Blueprint, render_template, session
from services.calendar_frontend_service import CalendarFrontendService
from services.course_frontend_service import CourseFrontendService

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/cronograma', methods=['GET'])
def calendar():

    id_curso = session.get("selected_course", 1)

    clases_api = CalendarFrontendService.get_all(id_curso)

    schedule = {}

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

    cursos = CourseFrontendService.get_all()

    return render_template(
        'calendar.html',
        schedule=sorted_schedule,
        cursos=cursos,
        selected_course=id_curso,
        active_page='calendar'
    )
