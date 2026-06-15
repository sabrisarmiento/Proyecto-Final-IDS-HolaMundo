from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.attendance_frontend_service import attendance_get_all, generate_qr, mark_attendance, get_class
from services.subjects_service import get_my_subjects
from services.courses_service import get_my_courses
from services.calendar_service import calendar_get_all

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/asistencia', methods=['GET'])
def attendance():
    subject_id = request.args.get('subject')
    course_id = request.args.get('curso')
    class_id = request.args.get('clase')

    subjects = get_my_subjects()
    courses = []
    classes = []
    attendance_records = []

    if subject_id:
        subject = next((s for s in subjects if str(s["id_materia"]) == subject_id), None)
        subject_name = subject.get("nombre") if subject else None
        courses = [c for c in get_my_courses() if c.get("materia") == subject_name]

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
    class_id = request.form.get('id_clase')
    horas = request.form.get('horas')
    minutos = request.form.get('minutos')
    result = generate_qr(class_id, horas, minutos)
    flash(result.get("message", "No se pudieron generar los QR."))

    course_id = request.form.get('course_id')
    if course_id:
        return redirect(url_for('courses.course_detail', course_id=course_id, tab='attendance', clase=class_id))

    subject_id = request.form.get('subject')
    curso_id = request.form.get('curso')
    return redirect(url_for('attendance.attendance', subject=subject_id, curso=curso_id, clase=class_id))

@attendance_bp.route('/presente', methods=['GET'])
def attendance_page():
    id_clase = request.args.get('id_clase')
    clase = get_class(id_clase)
    is_virtual = bool(clase) and clase.get("modalidad") == "Virtual"
    return render_template(
        'attendance_checkin.html',
        id_alumno=request.args.get('id_alumno'),
        id_clase=id_clase,
        code=request.args.get('code'),
        is_virtual=is_virtual,
    )

@attendance_bp.route('/presente/marcar', methods=['POST'])
def submit_attendance():
    payload = request.get_json(silent=True) or {}
    data, status = mark_attendance(payload)
    return jsonify(data), status