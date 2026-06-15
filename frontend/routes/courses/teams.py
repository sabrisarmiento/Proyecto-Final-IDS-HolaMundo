from flask import jsonify, redirect, request, session, url_for, flash
import requests
from . import courses_bp
from .common import BACKEND_URL, auth_headers

@courses_bp.route('/cursos/<int:course_id>/equipos/crear', methods=['POST'])
def create_team(course_id):
    try:
        response = requests.post(f"{BACKEND_URL}/equipos", headers=auth_headers(), json={
            "nombre_equipo": request.form.get("nombre_equipo"),
            "id_curso": course_id
        })
        if response.ok:
            flash("Equipo creado correctamente.", "success")
        elif response.status_code == 409:
            flash(response.json()["errors"][0]["description"], "error")
        else:
            flash("No se pudo crear el equipo.", "error")
    except Exception as e:
        print("Error creando equipo:", e)
        flash("Ocurrió un error al crear el equipo.", "error")
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))

@courses_bp.route('/cursos/<int:course_id>/equipos/eliminar', methods=['POST'])
def delete_teams(course_id):
    equipos = [t for t in request.form.get("selected_teams", "").split(",") if t]
    if not equipos:
        flash("No se seleccionó ningún equipo.", "warning")
        return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))
    try:
        for team_id in equipos:
            requests.delete(f"{BACKEND_URL}/equipos/{team_id}", headers=auth_headers())
        flash("Equipo eliminado correctamente." if len(equipos) == 1 else f"{len(equipos)} equipos eliminados correctamente.", "success")
    except Exception as e:
        print("Error eliminando equipos:", e)
        flash("No se pudieron eliminar los equipos.", "error")
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))

@courses_bp.route('/cursos/<int:course_id>/equipos/agregar-alumno', methods=['POST'])
def add_student_to_team(course_id):
    try:
        response = requests.post(f"{BACKEND_URL}/equipo-alumno", headers=auth_headers(), json={
            "id_equipo": request.form.get("id_equipo"),
            "padron": request.form.get("padron")
        })
        if response.status_code == 409:
            error = response.json()
            session["pending_team_change"] = {
                "mensaje": error["errors"][0]["description"],
                "padron": request.form.get("padron"),
                "id_equipo": request.form.get("id_equipo")
            }
    except Exception as e:
        print("Error agregando alumno al equipo:", e)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))

@courses_bp.route('/cursos/<int:course_id>/equipos/cambiar', methods=['POST'])
def change_student_team(course_id):
    try:
        requests.post(f"{BACKEND_URL}/equipo-alumno", headers=auth_headers(), json={
            "id_equipo": request.form.get("id_equipo"),
            "padron": request.form.get("padron"),
            "forzar": True
        })
        session.pop("pending_team_change", None)
    except Exception as e:
        print("Error cambiando alumno de equipo:", e)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))

@courses_bp.route('/cursos/<int:course_id>/equipos/cancelar-cambio', methods=['POST'])
def cancel_team_change(course_id):
    session.pop("pending_team_change", None)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))

@courses_bp.route('/cursos/<int:course_id>/equipos/quitar-alumno', methods=['POST'])
def remove_student_from_team(course_id):
    try:
        requests.delete(f"{BACKEND_URL}/equipo-alumno", headers=auth_headers(), json={
            "id_equipo": request.form.get("id_equipo"),
            "id_alumno": request.form.get("id_alumno")
        })
    except Exception as e:
        print("Error quitando alumno del equipo:", e)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))

@courses_bp.route('/cursos/<int:course_id>/buscar-alumno')
def buscar_alumno(course_id):
    try:
        response = requests.get(f"{BACKEND_URL}/students", headers=auth_headers(), params={
            "padron": request.args.get("padron"),
            "id_curso": course_id
        })
        students = response.json().get("students", []) if response.status_code != 204 else []
        if not students:
            return jsonify({"found": False})
        student = students[0]
        return jsonify({
            "found": True,
            "nombre": student["nombre"],
            "apellido": student["apellido"],
            "correo": student["correo"],
            "estado": "Activo" if student["estado_alumno"] else "Inactivo"
        })
    except Exception as e:
        print("Error buscando alumno:", e)
        return jsonify({"found": False, "error": str(e)}), 500