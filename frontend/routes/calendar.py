from flask import Blueprint, render_template, request
from services.subjects_service import get_subjects
from services.calendar_service import get_schedule_by_subject
from services.courses_service import get_courses

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/cronograma', methods=['GET'])
def calendar():
  view = request.args.get("subject")
  selected_course = request.args.get("course")
  schedule = []
  courses = []
  subjects = get_subjects()

  if view is not None:
    try:
      classes = get_schedule_by_subject(int(view))
      all_courses = get_courses()
      
      subject = next((s for s in subjects if s["id_materia"] == int(view)), None)
      subject_name = subject.get("nombre") if subject else None
      
      courses = [c for c in all_courses if c.get("materia") == subject_name]
      
      schedule_dict = {}
      for c in classes:
        week_num = c.get("semana")
        if week_num is not None:
          schedule_dict.setdefault(week_num, []).append(c)
      schedule = [{"week": week_num, "classes":
        schedule_dict[week_num]} for week_num in sorted(schedule_dict.keys())]
    except Exception as e:
      print(f"Error al obetener cronograma para la materia {view}: {e}")

  return render_template(
    'calendar.html',
    active_page='calendar',
    selected_subject=int(view) if view else None,
    selected_course=int(selected_course) if selected_course else None,
    subjects=subjects,
    schedule=schedule,
    courses=courses
  )