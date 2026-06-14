from flask import render_template, request, redirect, url_for, session
import requests

from . import courses_bp
from .common import BACKEND_URL, get_token, auth_headers
from services.courses_service import post_course
from services.subjects_service import get_my_subjects
from config import get_headers


@courses_bp.route('/cursos', methods=['GET', 'POST'])
def courses():
    subjects = get_my_subjects()

    if request.method == 'POST':
        try:
            data = {
                "catedra":      request.form.get('catedra'),
                "cuatrimestre": request.form.get('cuatrimestre'),
                "anio":         int(request.form.get('anio')),
                "id_materia":   int(request.form.get('id_materia')),
                "id_profesor":  int(request.form.get('id_profesor')),
            }
            post_course(data)
            return redirect(url_for('courses.courses'))
        except Exception as e:
            print(f"Error en cursos: {e}")

    filtro_materia = request.args.get('materia', '')
    filtro_catedra = request.args.get('catedra', '')
    filtro_anio = request.args.get('anio', '')
    filtro_cuatrimestre = request.args.get('cuatrimestre', '')

    try:
        params = {}
        if filtro_materia:
            params['materia'] = filtro_materia
        if filtro_anio:
            params['anio'] = filtro_anio
        response = requests.get(f'{BACKEND_URL}/courses/mias', params=params, headers=get_headers())
        data_courses = response.json().get('courses', []) if response.ok else []
    except Exception as e:
        print(f"Error cargando cursos: {e}")
        data_courses = []

    if filtro_catedra:
        data_courses = [c for c in data_courses if filtro_catedra.lower() in (c.get('catedra') or '').lower()]
    if filtro_cuatrimestre:
        data_courses = [c for c in data_courses if str(c.get('cuatrimestre', '')) == filtro_cuatrimestre]

    all_courses_raw = []
    try:
        all_courses_raw = requests.get(f'{BACKEND_URL}/courses/mias', headers=get_headers()).json().get('courses', [])
    except Exception:
        pass

    catedras_opciones      = sorted({c.get('catedra', '') for c in all_courses_raw if c.get('catedra')})
    anios_opciones         = sorted({str(c.get('anio', '')) for c in all_courses_raw if c.get('anio')}, reverse=True)
    cuatrimestres_opciones = sorted({str(c.get('cuatrimestre', '')) for c in all_courses_raw if c.get('cuatrimestre')})

    return render_template(
        'courses.html',
        courses=data_courses,
        subjects=subjects,
        active_page='courses',
        filtro_materia=filtro_materia,
        filtro_catedra=filtro_catedra,
        filtro_anio=filtro_anio,
        filtro_cuatrimestre=filtro_cuatrimestre,
        catedras_opciones=catedras_opciones,
        anios_opciones=anios_opciones,
        cuatrimestres_opciones=cuatrimestres_opciones,
    )


@courses_bp.route('/cursos/materias/crear', methods=['POST'])
def crear_materia():
    token = get_token()
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debés iniciar sesión')

    payload = {
        'nombre': request.form.get('nombre'),
        'codigo': request.form.get('codigo'),
    }
    try:
        requests.post(f'{BACKEND_URL}/subjects', json=payload, headers=auth_headers())
    except Exception as e:
        print(f"Error creando materia: {e}")

    return redirect(url_for('courses.courses'))


@courses_bp.route('/cursos/materias/<int:subject_id>/editar', methods=['POST'])
def editar_materia(subject_id):
    token = get_token()
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debés iniciar sesión')

    payload = {
        'nombre': request.form.get('nombre'),
        'codigo': request.form.get('codigo'),
    }
    try:
        requests.patch(f'{BACKEND_URL}/subjects/{subject_id}', json=payload, headers=auth_headers())
    except Exception as e:
        print(f"Error editando materia: {e}")

    return redirect(url_for('courses.courses'))


@courses_bp.route('/cursos/materias/<int:subject_id>/eliminar', methods=['POST'])
def eliminar_materia(subject_id):
    token = get_token()
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debés iniciar sesión')

    try:
        requests.delete(f'{BACKEND_URL}/subjects/{subject_id}', headers=auth_headers())
    except Exception as e:
        print(f"Error eliminando materia: {e}")

    return redirect(url_for('courses.courses'))


@courses_bp.route('/set-course/<int:course_id>')
def set_course(course_id):
    session['selected_course'] = course_id
    next_page = request.args.get('next')
    if next_page:
        return redirect(next_page)
    return redirect('/')


@courses_bp.route('/set-course/general')
def set_general():
    session.pop('selected_course', None)
    next_page = request.args.get('next')
    if next_page:
        return redirect(next_page)
    return redirect('/')