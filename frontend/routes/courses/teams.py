from flask import redirect, url_for, request, session
import requests

from . import courses_bp
from .common import BACKEND_URL, get_token, auth_headers


@courses_bp.route('/cursos/<int:course_id>/equipos/crear', methods=['POST'])
def create_team(course_id):
    try:
        data = {"nombre_equipo": request.form.get("nombre_equipo"), "id_curso": course_id}
        requests.post(f"{BACKEND_URL}/equipos", headers=auth_headers(), json=data)
    except Exception as e:
        print("Error creando equipo:", e)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))


@courses_bp.route('/cursos/<int:course_id>/equipos/agregar-alumno', methods=['POST'])
def add_student_to_team(course_id):
    try:
        data = {"id_equipo": request.form.get("id_equipo"), "padron": request.form.get("padron")}
        response = requests.post(f"{BACKEND_URL}/equipo-alumno", headers=auth_headers(), json=data)
        if response.status_code == 409:
            error = response.json()
            session["pending_team_change"] = {
                "mensaje":   error["errors"][0]["description"],
                "padron":    request.form.get("padron"),
                "id_equipo": request.form.get("id_equipo")
            }
    except Exception as e:
        print("Error agregando alumno:", e)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))


@courses_bp.route('/cursos/<int:course_id>/equipos/cambiar', methods=['POST'])
def change_student_team(course_id):
    try:
        data = {"id_equipo": request.form.get("id_equipo"), "padron": request.form.get("padron"), "forzar": True}
        requests.post(f"{BACKEND_URL}/equipo-alumno", headers=auth_headers(), json=data)
        session.pop("pending_team_change", None)
    except Exception as e:
        print("Error cambiando equipo:", e)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))


@courses_bp.route('/cursos/<int:course_id>/equipos/cancelar-cambio', methods=['POST'])
def cancel_team_change(course_id):
    session.pop('pending_team_change', None)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))


@courses_bp.route('/cursos/<int:course_id>/equipos/quitar-alumno', methods=['POST'])
def remove_student_from_team(course_id):
    try:
        data = {"id_equipo": request.form.get("id_equipo"), "id_alumno": request.form.get("id_alumno")}
        requests.delete(f"{BACKEND_URL}/equipo-alumno", headers=auth_headers(), json=data)
    except Exception as e:
        print("Error removing student:", e)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))