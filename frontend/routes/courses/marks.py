from flask import redirect, url_for, request, session, flash
import requests

from . import courses_bp
from .common import BACKEND_URL, get_token, auth_headers


@courses_bp.route('/cambiar-evaluacion', methods=['POST'])
def cambiar_evaluacion():
    eval_id   = request.form.get('eval_activa')
    course_id = request.form.get('course_id')
    if eval_id:
        session['eval_seleccionada'] = int(eval_id)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='marks'))


@courses_bp.route('/cursos/<int:course_id>/notas/guardar', methods=['POST'])
def guardar_notas(course_id):
    token = get_token()
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debes iniciar sesión')

    headers          = auth_headers()
    id_eval          = request.form.get('id_evaluacion')
    notas_dict       = {}
    correctores_dict = {}

    for key, value in request.form.items():
        if key.startswith('nota_alumno_') and value.strip():
            id_alumno = key.replace('nota_alumno_', '')
            try:
                notas_dict[id_alumno] = float(value)
            except ValueError:
                pass
        elif key.startswith('corrector_alumno_') and value.strip():
            id_alumno = key.replace('corrector_alumno_', '')
            correctores_dict[id_alumno] = value.strip()

    resp = requests.post(
        f'{BACKEND_URL}/notas/guardar',
        json={'id_evaluacion': id_eval, 'notas': notas_dict, 'correctores': correctores_dict},
        headers=headers
    )
    print(f"[guardar_notas] backend response: {resp.status_code} {resp.text}")

    return redirect(url_for('courses.course_detail', course_id=course_id, tab='marks'))


@courses_bp.route('/cursos/<int:course_id>/evaluaciones/crear', methods=['POST'])
def crear_evaluacion(course_id):
    token = get_token()
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debes iniciar sesión')
    nombre     = request.form.get('nombre_eval')
    asociacion = request.form.get('asociacion', 'Individual')
    requests.post(
        f'{BACKEND_URL}/evaluaciones',
        json={'id_curso': course_id, 'id_tipo': 1, 'nombre': nombre, 'asociacion': asociacion},
        headers=auth_headers()
    )
    session.pop('eval_seleccionada', None)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='marks'))


@courses_bp.route('/cursos/<int:course_id>/evaluaciones/eliminar/<int:eval_id>', methods=['POST'])
def eliminar_evaluacion(course_id, eval_id):
    token = get_token()
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debes iniciar sesión')

    requests.delete(f'{BACKEND_URL}/evaluaciones/{eval_id}', headers=auth_headers())
    if session.get('eval_seleccionada') == eval_id:
        session.pop('eval_seleccionada', None)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='marks'))


@courses_bp.route('/cursos/<int:course_id>/promocion/guardar', methods=['POST'])
def guardar_promocion(course_id):
    token = get_token()
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debes iniciar sesión')

    es_promocionable = request.form.get('es_promocionable') == '1'
    evaluaciones     = []

    for eval_id_str in request.form.getlist('eval_ids'):
        id_eval    = int(eval_id_str)
        cuenta     = f'cuenta_{id_eval}' in request.form
        nota_raw   = request.form.get(f'nota_minima_{id_eval}', '')
        nota_minima = float(nota_raw) if nota_raw != '' else None
        evaluaciones.append({'id_evaluacion': id_eval, 'cuenta': cuenta, 'nota_minima': nota_minima})

    try:
        requests.post(
            f'{BACKEND_URL}/cursos/{course_id}/promocion',
            json={'es_promocionable': es_promocionable, 'evaluaciones': evaluaciones},
            headers=auth_headers()
        )
    except Exception as e:
        print(f"Error guardando promo: {e}")

    return redirect(url_for('courses.course_detail', course_id=course_id, tab='marks'))


@courses_bp.route('/cursos/<int:course_id>/notas/grupal', methods=['POST'])
def asociar_nota_grupal(course_id):
    token = get_token()
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debes iniciar sesión')

    headers       = auth_headers()
    id_evaluacion = request.form.get('id_evaluacion')

    equipos_ids = [
        key.replace('id_equipo_', '')
        for key in request.form
        if key.startswith('id_equipo_')
    ]

    if not equipos_ids:
        flash('No se encontraron equipos en el formulario.', 'error')
        return redirect(url_for('courses.course_detail', course_id=course_id, tab='marks'))

    notas_dict       = {}
    correctores_dict = {}

    for id_equipo in equipos_ids:
        nota_raw  = request.form.get(f'nota_equipo_{id_equipo}', '').strip()
        corrector = request.form.get(f'corrector_equipo_{id_equipo}', '').strip()

        if not nota_raw:
            continue

        try:
            nota = float(nota_raw)
        except (ValueError, TypeError):
            continue

        try:
            team_res  = requests.get(f'{BACKEND_URL}/equipos/{id_equipo}', headers=headers)
            team_json = team_res.json()
            team_data = team_json.get('team') or {}
            alumnos = team_data.get('alumnos', [])
        except Exception as e:
            print(f"  Error obteniendo equipo {id_equipo}: {e}")
            continue

        for alumno in alumnos:
            aid = str(alumno['id_alumno'])
            notas_dict[aid] = nota
            if corrector:
                correctores_dict[aid] = corrector

    if not notas_dict:
        flash('No se ingresó ninguna nota válida o los equipos no tienen alumnos.', 'error')
        return redirect(url_for('courses.course_detail', course_id=course_id, tab='marks'))

    try:
        resp = requests.post(
            f'{BACKEND_URL}/notas/guardar',
            json={'id_evaluacion': id_evaluacion, 'notas': notas_dict, 'correctores': correctores_dict},
            headers=headers
        )
        print(f"[asociar_nota_grupal] backend response: {resp.status_code} {resp.text}")
        flash('Notas grupales guardadas correctamente.', 'ok')
    except Exception as e:
        print(f"Error guardando notas grupales: {e}")
        flash('Hubo un error al guardar las notas.', 'error')

    return redirect(url_for('courses.course_detail', course_id=course_id, tab='marks'))