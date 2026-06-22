from flask import redirect, url_for, request, session, flash, jsonify, Response
import requests

from . import courses_bp
from .common import BACKEND_URL, get_token, auth_headers
from services.students_services import patch_student
from services.material_frontend_service import create_material, update_material, delete_material

@courses_bp.route('/cursos/<int:course_id>/importar-alumnos', methods=['POST'])
def importar_alumnos(course_id):
    token = get_token()
    if not token:
        return redirect(url_for('login.login'))

    file = request.files.get('file')
    if not file:
        flash("No se seleccionó ningún archivo.", "error")
        return redirect(url_for('courses.course_detail', course_id=course_id, tab='students'))

    try:
        backend_res = requests.post(
            f'{BACKEND_URL}/students/import',
            headers=auth_headers(),
            files={'file': (file.filename, file.stream, 'text/csv')},
            data={'id_curso': course_id},
        )
        data = backend_res.json()
        if data.get('creados') is not None:
            creados = data['creados']
            errores = data.get('errores', 0)
            if creados > 0:
                msg = f"Se importaron {creados} alumno(s)."
                if errores:
                    msg += f" {errores} fila(s) con error."
                flash(msg, "success")
            else:
                detalle = data.get('detalle_errores') or []
                if detalle:
                    primer = detalle[0]
                    flash(f"Fila {primer.get('fila', '?')}: {primer.get('error', 'Error desconocido')}", "error")
                else:
                    flash("No se pudo importar ningún alumno.", "error")
        else:
            error = (data.get('errors') or [{}])[0].get('description') or data.get('error') or "No se pudo importar el archivo."
            flash(error, "error")
    except Exception as e:
        flash(f"No se pudo importar: {e}", "error")

    return redirect(url_for('courses.course_detail', course_id=course_id, tab='students'))


@courses_bp.route('/cursos/<int:course_id>/exportar-informes', methods=['GET'])
def exportar_informes(course_id):
    token = get_token()
    if not token:
        return redirect(url_for('auth.login'))

    params = [('curso_id', course_id)]
    for seccion in ('alumnos', 'equipos', 'notas', 'asistencia', 'mostrar_corrector', 'incluir_estado_final'):
        if request.args.get(seccion) in ('1', 'true', 'on'):
            params.append((seccion, '1'))
    for ev in request.args.getlist('evaluaciones[]'):
        params.append(('evaluaciones[]', ev))
    for field in ('materia', 'catedra', 'cuatrimestre', 'anio'):
        val = request.args.get(field)
        if val:
            params.append((field, val))

    try:
        backend_res = requests.get(
            f'{BACKEND_URL}/reportes/exportar',
            headers=auth_headers(),
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


@courses_bp.route('/cursos/<int:course_id>/dashboard-data', methods=['GET'])
def course_dashboard_data(course_id):
    try:
        token   = get_token()
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        res     = requests.get(f'{BACKEND_URL}/cursos/{course_id}/dashboard', headers=headers)
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 502


@courses_bp.route('/cursos/<int:course_id>/estudiantes/<int:student_id>', methods=['POST'])
def edit_student(course_id, student_id):
    try:
        if request.form.get('form_type') == 'estado':
            valores = request.form.getlist('estado_alumno')
            data = {"estado_alumno": valores[-1] == '1'}
        else:
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
    token = get_token()
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debes iniciar sesión')

    headers = auth_headers()
    data    = {
        'catedra':      request.form.get('catedra'),
        'cuatrimestre': request.form.get('cuatrimestre'),
        'anio':         int(request.form.get('anio')),
        'slack_url': request.form.get('slack_url', '').strip(),
        'youtube_url': request.form.get('youtube_url', '').strip(),
        'regimen_aprobacion': request.form.get('regimen_aprobacion', '').strip(),
    }   

    try:
        res = requests.patch(f'{BACKEND_URL}/courses/{course_id}', json=data, headers=headers)
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


@courses_bp.route('/cursos/<int:course_id>/temas', methods=['POST'])
def update_temas(course_id):
    token = get_token()
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debes iniciar sesión')

    id_materia = request.form.get('id_materia')
    nombres = request.form.getlist('temas_nombre[]')
    iconos = request.form.getlist('temas_icono[]')
    temas = [{"nombre": n, "icono": i} for n, i in zip(nombres, iconos) if n.strip()]

    try:
        requests.put(
            f'{BACKEND_URL}/subjects/{id_materia}/temas',
            json={"temas": temas},
            headers=auth_headers()
        )
        session['config_msg'] = 'Temas actualizados correctamente'
        session['config_ok'] = True
    except Exception as e:
        session['config_msg'] = f'Error al actualizar temas: {e}'
        session['config_ok'] = False

    return redirect(url_for('courses.course_detail', course_id=course_id, tab='config'))


@courses_bp.route('/cursos/<int:course_id>/materiales', methods=['POST'])
def create_material_view(course_id):
    data = {
        "titulo": request.form.get('titulo'),
        "descripcion": request.form.get('descripcion'),
        "url_externo": request.form.get('url_externo'),
        "id_curso": course_id,
        "id_clase": request.form.get('id_clase') or None,
    }
    result, status = create_material(data)
    if status >= 400:
        flash(result.get("errors", [{}])[0].get("description", "No se pudo crear el material."))
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='materials'))

@courses_bp.route('/cursos/<int:course_id>/materiales/<int:id_material>/editar', methods=['POST'])
def editar_material_view(course_id, id_material):
    data = {
        "titulo": request.form.get('titulo'),
        "descripcion": request.form.get('descripcion'),
        "url_externo": request.form.get('url_externo'),
        "id_clase": request.form.get('id_clase') or None,
    }
    result, status = update_material(id_material, data)
    if status >= 400:
        flash(result.get("errors", [{}])[0].get("description", "No se pudo editar el material."))
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='materials'))


@courses_bp.route('/cursos/<int:course_id>/materiales/<int:id_material>/eliminar', methods=['POST'])
def eliminar_material_view(course_id, id_material):
    result, status = delete_material(id_material)
    if status >= 400:
        flash(result.get("errors", [{}])[0].get("description", "No se pudo eliminar el material."))
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='materials'))

@courses_bp.route('/cursos/<int:course_id>/eliminar', methods=['POST'])
def delete_course_route(course_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debes iniciar sesión')

    headers = {'Authorization': f'Bearer {token}'}
    try:
        res = requests.delete(
            f'http://127.0.0.1:5000/courses/{course_id}',
            headers=headers
        )
        if res.status_code == 200:
            return redirect(url_for('courses.courses'))
        else:
            return redirect(url_for('courses.course_detail', course_id=course_id, tab='config'))
    except Exception as e:
        return redirect(url_for('courses.course_detail', course_id=course_id, tab='config'))
