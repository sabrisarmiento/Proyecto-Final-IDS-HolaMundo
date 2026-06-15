from flask import redirect, url_for, request, session, flash
import requests

from . import courses_bp
from .common import BACKEND_URL, get_token, auth_headers


@courses_bp.route('/cursos/<int:course_id>/clases/crear', methods=['POST'])
def crear_clase(course_id):
    token = get_token()
    if not token:
        return redirect(url_for('auth.login'))

    headers = auth_headers()
    data = {
        "fecha": request.form.get("fecha_clase"),
        "semana": request.form.get("semana"),
        "temas": request.form.get("temas"),
        "tipo": request.form.get("tipo"),
        "modalidad": request.form.get("modalidad"),
        "id_curso": course_id
    }

    if not data['fecha'] or not data['semana'] or not data['temas'] or not data['tipo'] or not data['modalidad']:
        flash('Falta ingresar datos.', 'error')
        return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))

    try:
        clases_res  = requests.get(f'{BACKEND_URL}/clases?id_curso={course_id}')
        clases_json = clases_res.json()
        clases = clases_json.get("classes", [])

        tema_nuevo = data["temas"].strip().lower()
        fecha_nueva = data["fecha"]
        semana_nueva = int(data["semana"])
        semana_anterior_existe = False

        for clase in clases:
            tema_existente = clase.get("temas", "").strip().lower()
            fecha_existente = clase.get("fecha", "")
            if int(clase.get("semana", 0)) == semana_nueva - 1:
                semana_anterior_existe = True
            if tema_existente == tema_nuevo:
                flash('Ya existe una clase con ese tema', 'error')
                return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))
            if fecha_existente == fecha_nueva:
                flash('Ya existe una clase con esa fecha', 'error')
                return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))

        if semana_nueva > 1 and not semana_anterior_existe:
            flash(f'Debe existir una clase en la semana {semana_nueva - 1}.', 'error')
            return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))

        res = requests.post(f'{BACKEND_URL}/clases', json=data, headers=headers)
        if res.status_code == 201:
            flash('Clase creada correctamente.', 'success')
        else:
            flash('Error al crear la clase', 'error')
    except Exception as e:
        print(f"Error guardando clase: {e}")
        flash('Hubo un error al guardar la clase.', 'error')

    return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))


@courses_bp.route('/cursos/<int:course_id>/clases/<int:id_clase>/editar', methods=['POST'])
def editar_clase(course_id, id_clase):
    token = get_token()
    headers = auth_headers()

    data = {
        "fecha": request.form.get("fecha_clase"),
        "semana": request.form.get("semana"),
        "temas": request.form.get("temas"),
        "tipo": request.form.get("tipo"),
        "modalidad": request.form.get("modalidad"),
        "id_curso": course_id
    }

    if not data['fecha'] or not data['semana'] or not data['temas'] or not data['tipo'] or not data['modalidad']:
        flash('Falta ingresar datos.', 'error')
        return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))

    try:
        clases_res  = requests.get(f'{BACKEND_URL}/clases?id_curso={course_id}')
        clases_json = clases_res.json()
        clases = clases_json.get("classes", [])

        tema_nuevo = data["temas"].strip().lower()
        fecha_nueva = data["fecha"]
        semana_nueva = int(data["semana"])
        semana_anterior_existe = False

        for clase in clases:
            if clase["id_clase"] == id_clase:
                continue
            tema_existente = clase.get("temas", "").strip().lower()
            fecha_existente = clase.get("fecha", "")
            if int(clase.get("semana", 0)) == semana_nueva - 1:
                semana_anterior_existe = True
            if tema_existente == tema_nuevo:
                flash('Ya existe una clase con ese tema', 'error')
                return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))
            if fecha_existente == fecha_nueva:
                flash('Ya existe una clase con esa fecha', 'error')
                return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))

        if semana_nueva > 1 and not semana_anterior_existe:
            flash(f'Debe existir una clase en la semana {semana_nueva - 1}.', 'error')
            return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))

        res = requests.patch(f'{BACKEND_URL}/clases/{id_clase}', json=data, headers=headers)
        if res.status_code == 200:
            flash('Clase actualizada correctamente', 'success')
        else:
            flash('Hubo un error al actualizar la clase', 'error')

    except Exception as e:
        print(e)
        flash('Hubo un error al actualizar la clase', 'error')

    return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))


@courses_bp.route('/cursos/<int:course_id>/clases/<int:id_clase>/eliminar', methods=['GET'])
def eliminar_clase(course_id, id_clase):
    headers = auth_headers()
    requests.delete(f'{BACKEND_URL}/clases/{id_clase}', headers=headers)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))