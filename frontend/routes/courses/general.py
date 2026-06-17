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

    assigned_subjects = []

    try:
        response = requests.get(
            f'{BACKEND_URL}/subjects/my-assigned',
            headers=get_headers()
        )
        assigned_subjects = response.json().get('subjects', []) if response.ok else []
    except Exception as e:
        print(f"Error cargando materias asignadas: {e}")

    if request.method == 'POST':
        try:
            user = session.get("user", {})
            id_profesor = user.get("id_usuario")
            data = {
                "catedra":      request.form.get('catedra'),
                "cuatrimestre": request.form.get('cuatrimestre'),
                "anio":         int(request.form.get('anio')),
                "id_materia":   int(request.form.get('id_materia')),
                "id_profesor":  int(id_profesor),
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

    user = session.get("user", {})
    try:
        nivel = int(user.get("nivel", 0))
    except (TypeError, ValueError):
        nivel = 0
    es_superadmin = nivel >= 3

    return render_template(
        'courses.html',
        courses=data_courses,
        assigned_subjects=assigned_subjects,
        subjects=subjects,
        nivel=nivel,
        es_superadmin=es_superadmin,
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

@courses_bp.route('/cursos/materias/<int:subject_id>/profesores', methods=['GET', 'POST'])
def profesores_materia(subject_id):
    token = get_token()

    if not token:
        return redirect(url_for('landing.landing') + '?error=Debés iniciar sesión')

    if request.method == 'POST':
        id_profesor = request.form.get('id_profesor')

        payload = {
            'id_profesor': id_profesor
        }

        try:
            requests.post(
                f'{BACKEND_URL}/subjects/{subject_id}/professors',
                json=payload,
                headers=auth_headers()
            )
        except Exception as e:
            print(f"Error asignando profesor a materia: {e}")

        return redirect(url_for(
            'courses.profesores_materia',
            subject_id=subject_id
        ))

    try:
        subject_res = requests.get(
            f'{BACKEND_URL}/subjects/{subject_id}',
            headers=auth_headers()
        )
        subject_data = subject_res.json() if subject_res.ok else {}
        subject = subject_data.get('subject') or subject_data.get('data') or {}
    except Exception as e:
        print(f"Error obteniendo materia: {e}")
        subject = {}

    try:
        assigned_res = requests.get(
            f'{BACKEND_URL}/subjects/{subject_id}/professors',
            headers=auth_headers()
        )
        assigned_data = assigned_res.json() if assigned_res.ok else {}
        assigned_professors = assigned_data.get('professors') or assigned_data.get('data') or []
    except Exception as e:
        print(f"Error obteniendo profesores asignados: {e}")
        assigned_professors = []

    try:
        professors_res = requests.get(
            f'{BACKEND_URL}/users',
            params={'id_rol': 2},
            headers=auth_headers()
        )
        professors_data = professors_res.json() if professors_res.ok else {}
        professors = professors_data.get('users') or professors_data.get('data') or []
    except Exception as e:
        print(f"Error obteniendo profesores: {e}")
        professors = []

    return render_template(
        'subject_professors.html',
        subject=subject,
        assigned_professors=assigned_professors,
        professors=professors
    )

@courses_bp.route('/cursos/materias/<int:subject_id>/profesores/<int:professor_id>/quitar', methods=['POST'])
def quitar_profesor_materia(subject_id, professor_id):
    token = get_token()

    if not token:
        return redirect(url_for('landing.landing') + '?error=Debés iniciar sesión')

    try:
        requests.delete(
            f'{BACKEND_URL}/subjects/{subject_id}/professors/{professor_id}',
            headers=auth_headers()
        )
    except Exception as e:
        print(f"Error quitando profesor de materia: {e}")

    return redirect(url_for(
        'courses.profesores_materia',
        subject_id=subject_id
    ))



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