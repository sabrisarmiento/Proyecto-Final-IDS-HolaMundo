from flask import Blueprint, render_template, request, redirect, url_for
from services.attendance_frontend_service import attendance_get_all, generate_qr
from services.subjects_service import get_subjects
from services.courses_service import get_courses
from services.calendar_service import calendar_get_all

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/asistencia', methods=['GET'])
def attendance():
    subject_id = request.args.get('subject')
    course_id = request.args.get('curso')
    class_id = request.args.get('clase')

    subjects = get_subjects()
    courses = []
    classes = []
    attendance_records = []

    if subject_id:
        subject = next((s for s in subjects if str(s["id_materia"]) == subject_id), None)
        subject_name = subject.get("nombre") if subject else None
        courses = [c for c in get_courses() if c.get("materia") == subject_name]

    if course_id:
        classes = calendar_get_all(course_id)

    if class_id:
        attendance_records = attendance_get_all(class_id)

    return render_template(
        "attendance.html",
        active_page='attendance',
        subjects=subjects,
        courses=courses,
        classes=classes,
        attendance=attendance_records,
        subject_id=subject_id,
        course_id=course_id,
        class_id=class_id,
    )


@attendance_bp.route('/asistencia/generar-qr', methods=['POST'])
def generate_qr_view():
    subject_id = request.form.get('subject')
    course_id = request.form.get('curso')
    class_id = request.form.get('id_clase')
    generate_qr(class_id)
    return redirect(url_for('attendance.attendance', subject=subject_id, curso=course_id, clase=class_id))