from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, Response

import requests
from services.advertisements_service import get_advertisements_by_course
from services.courses_service import get_courses, get_course_by_id, post_course
from services.students_services import post_student, patch_student
from services.exams_service import get_exams_by_course_id
from services.subjects_service import get_subjects

BACKEND_URL = 'http://127.0.0.1:5000'

courses_bp = Blueprint('courses', __name__)


@courses_bp.route('/cursos', methods=['GET', 'POST'])
def courses():
    subjects = get_subjects()

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
        response = requests.get(f'{BACKEND_URL}/courses', params=params)
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
        all_courses_raw = requests.get(f'{BACKEND_URL}/courses').json().get('courses', [])
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
    token = session.get('token')
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debés iniciar sesión')

    payload = {
        'nombre': request.form.get('nombre'),
        'codigo': request.form.get('codigo'),
    }
    try:
        requests.post(
            f'{BACKEND_URL}/subjects',
            json=payload,
            headers={'Authorization': f'Bearer {token}'}
        )
    except Exception as e:
        print(f"Error creando materia: {e}")

    return redirect(url_for('courses.courses'))


@courses_bp.route('/cursos/materias/<int:subject_id>/editar', methods=['POST'])
def editar_materia(subject_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debés iniciar sesión')

    payload = {
        'nombre': request.form.get('nombre'),
        'codigo': request.form.get('codigo'),
    }
    try:
        requests.patch(
            f'{BACKEND_URL}/subjects/{subject_id}',
            json=payload,
            headers={'Authorization': f'Bearer {token}'}
        )
    except Exception as e:
        print(f"Error editando materia: {e}")

    return redirect(url_for('courses.courses'))


@courses_bp.route('/cursos/materias/<int:subject_id>/eliminar', methods=['POST'])
def eliminar_materia(subject_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debés iniciar sesión')

    try:
        requests.delete(
            f'{BACKEND_URL}/subjects/{subject_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
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

@courses_bp.route('/cursos/<int:course_id>', methods=['GET', 'POST'])
def course_detail(course_id):
    active_tab = request.args.get('tab', 'general')
    page       = request.args.get('page', 1, type=int)
    per_page   = 10
    order_by   = request.args.get('order_by')
    order      = request.args.get('order')

    token   = session.get('token')
    headers = {'Authorization': f'Bearer {token}'}

    try:
        course = get_course_by_id(course_id)
    except Exception:
        course = {}

    try:
        evaluaciones = get_exams_by_course_id(course_id)
    except Exception:
        evaluaciones = []

    try:
        tipos_res      = requests.get(f'{BACKEND_URL}/tipos-evaluacion')
        tipos_evaluacion = tipos_res.json().get("exam_types", [])
    except Exception as e:
        print(f"Error loading tipos de evaluacion: {e}")
        tipos_evaluacion = []

    try:
        params = {'id_curso': course_id, 'page': page, 'per_page': per_page}
        if order_by:
            params['order_by'] = order_by
        if order:
            params['order'] = order

        students_res  = requests.get(f'http://127.0.0.1:5000/students_with_notes', params=params, headers=headers)
        response_data = students_res.json()
        students_data = response_data.get('data') or response_data.get('students') or []
        total         = response_data.get('total', len(students_data))
    except Exception:
        students_data = []
        total         = 0

    try:
        clases_res  = requests.get(f'http://127.0.0.1:5000/clases?id_curso={course_id}')
        clases      = clases_res.json().get("classes", [])
    except Exception as e:
        print(f"Error cargando clases: {e}")
        clases = []

    for s in students_data:
        notas_dict = {}
        raw_string = s.get('notas_raw') or ""
        if raw_string:
            for par in raw_string.split(','):
                if ':' in par:
                    id_ev, nota = par.split(':', 1)
                    try:
                        notas_dict[int(id_ev.strip())] = nota.strip()
                    except ValueError:
                        pass
        s['notas_todas'] = notas_dict
        s['notas_json']  = {str(k): v for k, v in notas_dict.items()}

        correctores_dict = {}
        raw_corr = s.get('correctores_raw') or ""
        if raw_corr:
            for par in raw_corr.split(','):
                if ':' in par:
                    id_ev, nombre_corr = par.split(':', 1)
                    try:
                        val = nombre_corr.strip()
                        if val:
                            correctores_dict[int(id_ev.strip())] = val
                    except ValueError:
                        pass
        s['correctores_todas'] = correctores_dict

        if not s.get('promedio_final') and notas_dict:
            valores = [float(v) for v in notas_dict.values() if v not in ('', None)]
            s['promedio_final'] = round(sum(valores) / len(valores), 1) if valores else None

    eval_id_sel    = session.get('eval_seleccionada')
    eval_seleccionada = next((e for e in evaluaciones if e['id_evaluacion'] == eval_id_sel), None)
    if not eval_seleccionada and evaluaciones:
        eval_seleccionada = evaluaciones[0]

    promedio_eval = 0.0
    if eval_seleccionada:
        notas_activa = []
        for s in students_data:
            n = s.get('notas_todas', {}).get(eval_seleccionada['id_evaluacion'])
            if n not in (None, ''):
                try:
                    notas_activa.append(float(n))
                except ValueError:
                    pass
        promedio_eval = round(sum(notas_activa) / len(notas_activa), 1) if notas_activa else 0.0

    todos_los_valores = []
    for s in students_data:
        for nota in (s.get('notas_todas') or {}).values():
            if nota not in (None, ''):
                try:
                    todos_los_valores.append(float(nota))
                except ValueError:
                    pass
    promedio_general = round(sum(todos_los_valores) / len(todos_los_valores), 1) if todos_los_valores else 0.0

    total_pages = max(1, (total + per_page - 1) // per_page)

    try:
        teams_res = requests.get(f'http://127.0.0.1:5000/equipos?id_curso={course_id}', headers=headers)
        teams_json = teams_res.json()
        teams = teams_json.get("teams") or teams_json.get("data") or []
    except Exception as e:
        print(f"Error loading teams: {e}")
        teams = []

    try:
        promo_res  = requests.get(f'http://127.0.0.1:5000/cursos/{course_id}/promocion', headers=headers)
        promo_data = promo_res.json().get('config', {})
        curso_es_promocionable = promo_data.get('es_promocionable', False)
        promo_evals  = promo_data.get('evaluaciones', [])
        promo_config = {}
        for p in promo_evals:
            promo_config[p['id_evaluacion']] = {
                'cuenta':      bool(p.get('cuenta_para_promocion')),
                'nota_minima': p.get('nota_minima')
            }
    except Exception:
        curso_es_promocionable = False
        promo_config           = {}

    pending_team_change = session.get("pending_team_change")

    try:
        advertisements = get_advertisements_by_course(course_id)
    except Exception:
        advertisements = []

    try:
        dash_res  = requests.get(f'http://127.0.0.1:5000/cursos/{course_id}/dashboard', headers=headers)
        dash_data = dash_res.json().get('dashboard', {}) if dash_res.ok else {}
    except Exception:
        dash_data = {}

    return render_template(
        'course_detail.html',
        course=course,
        students=students_data,
        teams=teams,
        clases=clases,
        active_page='courses',
        page=page,
        total_pages=total_pages,
        course_id=course_id,
        active_tab=active_tab,
        evaluaciones=evaluaciones,
        tipos_evaluacion=tipos_evaluacion,
        eval_seleccionada=eval_seleccionada,
        promedio_eval=promedio_eval,
        promedio_general=promedio_general,
        curso_es_promocionable=curso_es_promocionable,
        promo_config=promo_config,
        pending_team_change=pending_team_change,
        advertisements=advertisements,
        config_msg=session.pop('config_msg', None),
        config_ok=session.pop('config_ok', False),
        dash_data=dash_data
    )

@courses_bp.route('/cursos/<int:course_id>/buscar-alumno')
def buscar_alumno(course_id):
    headers = {'Authorization': f"Bearer {session.get('token')}"}
    params = {'padron': request.args.get('padron'), 'id_curso': course_id}
    try:
        res = requests.get('http://127.0.0.1:5000/students', params=params, headers=headers)
        alumnos = res.json().get("students", []) if res.status_code != 204 else []
        if not alumnos:
            return jsonify({"found": False})
        al = alumnos[0]
        return jsonify({
            "found": True,
            "nombre": al["nombre"],
            "apellido": al["apellido"],
            "correo": al["correo"],
            "estado": "Activo" if al["estado_alumno"] else "Inactivo"
        })
    except Exception as e:
        print("ERROR BUSCAR ALUMNO:", e)
        return jsonify({"found": False, "error": str(e)}), 500

@courses_bp.route('/cursos/<int:course_id>/equipos/crear', methods=['POST'])
def create_team(course_id):
    try:
        token   = session.get('token')
        headers = {'Authorization': f'Bearer {token}'}
        data    = {"nombre_equipo": request.form.get("nombre_equipo"), "id_curso": course_id}
        requests.post("http://127.0.0.1:5000/equipos", headers=headers, json=data)
    except Exception as e:
        print("Error creando equipo:", e)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))


@courses_bp.route('/cursos/<int:course_id>/equipos/agregar-alumno', methods=['POST'])
def add_student_to_team(course_id):
    try:
        token    = session.get('token')
        headers  = {'Authorization': f'Bearer {token}'}
        data     = {"id_equipo": request.form.get("id_equipo"), "padron": request.form.get("padron")}
        response = requests.post("http://127.0.0.1:5000/equipo-alumno", headers=headers, json=data)
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
        token   = session.get('token')
        headers = {'Authorization': f'Bearer {token}'}
        data    = {"id_equipo": request.form.get("id_equipo"), "padron": request.form.get("padron"), "forzar": True}
        requests.post("http://127.0.0.1:5000/equipo-alumno", headers=headers, json=data)
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
        token   = session.get('token')
        headers = {'Authorization': f'Bearer {token}'}
        data    = {"id_equipo": request.form.get("id_equipo"), "id_alumno": request.form.get("id_alumno")}
        requests.delete("http://127.0.0.1:5000/equipo-alumno", headers=headers, json=data)
    except Exception as e:
        print("Error removing student:", e)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))

@courses_bp.route('/cursos/<int:course_id>/equipos/eliminar', methods=['POST'])
def delete_teams(course_id):
    headers = {"Authorization": f"Bearer {session.get('token')}"}
    equipos = [t for t in request.form.get("selected_teams", "").split(",") if t]
    for team_id in equipos:
        try:
            requests.delete(f"http://127.0.0.1:5000/equipos/{team_id}", headers=headers)
        except Exception as e:
            print(f"Error eliminando equipo {team_id}: {e}")
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))

@courses_bp.route('/cursos/<int:course_id>/importar-alumnos', methods=['POST'])
def importar_alumnos(course_id):
    token = session.get('token')
    if not token:
        return jsonify({"error": "No autenticado"}), 401

    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No se seleccionó ningún archivo"}), 400

    try:
        backend_res = requests.post(
            f'{BACKEND_URL}/students/import',
            headers={'Authorization': f'Bearer {token}'},
            files={'file': (file.filename, file.stream, 'text/csv')},
            data={'id_curso': course_id},
        )
        return jsonify(backend_res.json()), backend_res.status_code
    except Exception as e:
        return jsonify({"error": f"No se pudo importar: {e}"}), 500


@courses_bp.route('/cursos/<int:course_id>/exportar-informes', methods=['GET'])
def exportar_informes(course_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('auth.login'))

    params = [('curso_id', course_id)]
    for seccion in ('alumnos', 'equipos', 'notas'):
        if request.args.get(seccion) in ('1', 'true', 'on'):
            params.append((seccion, '1'))
    for ev in request.args.getlist('evaluaciones[]'):
        params.append(('evaluaciones[]', ev))

    try:
        backend_res = requests.get(
            f'{BACKEND_URL}/reportes/exportar',
            headers={'Authorization': f'Bearer {token}'},
            params=params,
        )
    except Exception as e:
        return f"No se pudo generar el informe: {e}", 500

    if backend_res.status_code != 200:
        return Response(backend_res.content, status=backend_res.status_code,
                        content_type=backend_res.headers.get('Content-Type', 'application/json'))

    return Response(
        backend_res.content,
        mimetype='application/pdf',
        headers={'Content-Disposition': f'attachment; filename="informe_curso_{course_id}.pdf"'},
    )


@courses_bp.route('/cambiar-evaluacion', methods=['POST'])
def cambiar_evaluacion():
    eval_id   = request.form.get('eval_activa')
    course_id = request.form.get('course_id')
    if eval_id:
        session['eval_seleccionada'] = int(eval_id)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='marks'))


@courses_bp.route('/cursos/<int:course_id>/notas/guardar', methods=['POST'])
def guardar_notas(course_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debes iniciar sesión')

    headers    = {'Authorization': f'Bearer {token}'}
    id_eval    = request.form.get('id_evaluacion')
    notas_dict = {}
    correctores_dict = {}

    for key, value in request.form.items():
        if key.startswith('nota_') and value:
            id_alumno = key.replace('nota_', '')
            try:
                notas_dict[id_alumno] = float(value)
            except ValueError:
                pass
        elif key.startswith('corrector_') and value:
            id_alumno = key.replace('corrector_', '')
            correctores_dict[id_alumno] = value

    requests.post(
        'http://127.0.0.1:5000/notas/guardar',
        json={'id_evaluacion': id_eval, 'notas': notas_dict, 'correctores': correctores_dict},
        headers=headers
    )
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='marks'))


@courses_bp.route('/cursos/<int:course_id>/evaluaciones/crear', methods=['POST'])
def crear_evaluacion(course_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debes iniciar sesión')

    nombre  = request.form.get('nombre_eval')
    headers = {'Authorization': f'Bearer {token}'}
    requests.post(
        'http://127.0.0.1:5000/evaluaciones',
        json={'id_curso': course_id, 'id_tipo': 1, 'nombre': nombre},
        headers=headers
    )
    session.pop('eval_seleccionada', None)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='marks'))


@courses_bp.route('/cursos/<int:course_id>/evaluaciones/eliminar/<int:eval_id>', methods=['POST'])
def eliminar_evaluacion(course_id, eval_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debes iniciar sesión')

    headers = {'Authorization': f'Bearer {token}'}
    requests.delete(f'http://127.0.0.1:5000/evaluaciones/{eval_id}', headers=headers)
    if session.get('eval_seleccionada') == eval_id:
        session.pop('eval_seleccionada', None)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='marks'))


@courses_bp.route('/cursos/<int:course_id>/promocion/guardar', methods=['POST'])
def guardar_promocion(course_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debes iniciar sesión')

    headers          = {'Authorization': f'Bearer {token}'}
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
            f'http://127.0.0.1:5000/cursos/{course_id}/promocion',
            json={'es_promocionable': es_promocionable, 'evaluaciones': evaluaciones},
            headers=headers
        )
    except Exception as e:
        print(f"Error guardando promo: {e}")

    return redirect(url_for('courses.course_detail', course_id=course_id, tab='marks'))


@courses_bp.route('/cursos/<int:course_id>/dashboard-data', methods=['GET'])
def course_dashboard_data(course_id):
    try:
        token   = session.get('token')
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        res     = requests.get(f'http://127.0.0.1:5000/cursos/{course_id}/dashboard', headers=headers)
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 502


@courses_bp.route('/cursos/<int:course_id>/clases/crear', methods=['POST'])
def crear_clase(course_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('auth.login'))

    headers = {'Authorization': f'Bearer {token}'}
    data    = request.get_json()
    data['id_curso'] = course_id
    response = requests.post('http://127.0.0.1:5000/clases', json=data, headers=headers)
    return response.json(), response.status_code


@courses_bp.route('/cursos/<int:course_id>/clases/<int:id_clase>/eliminar', methods=['DELETE'])
def eliminar_clase(course_id, id_clase):
    token    = session.get('token')
    headers  = {'Authorization': f'Bearer {token}'}
    response = requests.delete(f'http://127.0.0.1:5000/clases/{id_clase}', headers=headers)
    return response.json(), response.status_code


@courses_bp.route('/cursos/<int:course_id>/estudiantes/<int:student_id>', methods=['POST'])
def edit_student(course_id, student_id):
    try:
        data = {
            "nombre":   request.form.get('nombre'),
            "apellido": request.form.get('apellido'),
            "padron":   int(request.form.get('padron')),
            "correo":   request.form.get('correo'),
        }
        patch_student(student_id, data)
    except Exception as e:
        print(e)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='students'))


@courses_bp.route('/cursos/<int:course_id>/configuracion', methods=['POST'])
def update_course_config(course_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debes iniciar sesión')

    headers = {'Authorization': f'Bearer {token}'}
    data    = {
        'catedra':      request.form.get('catedra'),
        'cuatrimestre': request.form.get('cuatrimestre'),
        'anio':         int(request.form.get('anio')),
    }
    slack_url   = request.form.get('slack_url', '').strip()
    youtube_url = request.form.get('youtube_url', '').strip()
    if slack_url:
        data['slack_url'] = slack_url
    if youtube_url:
        data['youtube_url'] = youtube_url

    try:
        res = requests.patch(f'http://127.0.0.1:5000/courses/{course_id}', json=data, headers=headers)
        if res.status_code == 200:
            session['config_msg'] = 'Configuración guardada correctamente'
            session['config_ok']  = True
        else:
            session['config_msg'] = 'No se pudo guardar la configuración'
            session['config_ok']  = False
    except Exception as e:
        session['config_msg'] = f'Error de conexión: {e}'
        session['config_ok']  = False

    return redirect(url_for('courses.course_detail', course_id=course_id, tab='config'))
