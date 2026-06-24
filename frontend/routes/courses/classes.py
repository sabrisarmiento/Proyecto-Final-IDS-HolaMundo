from flask import redirect, url_for, request, session, flash
from services.classes_service import get_classes_by_course, post_clase, patch_clase, delete_clase
from . import courses_bp
from .common import get_token


@courses_bp.route('/cursos/<int:course_id>/clases/crear', methods=['POST'])
def crear_clase(course_id):
    if not get_token():
        return redirect(url_for('auth.login'))

    user = session.get("user", {})
    data = {
        "fecha": request.form.get("fecha_clase"),
        "semana": request.form.get("semana"),
        "temas": request.form.get("temas"),
        "tipo": request.form.get("tipo"),
        "modalidad": request.form.get("modalidad"),
        "id_curso": course_id,
        "id_creador_clase": user.get("id_usuario")
    }

    if not all([data['fecha'], data['semana'], data['temas'], data['tipo'], data['modalidad']]):
        flash('Falta ingresar datos.', 'error')
        return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))

    result = get_classes_by_course(course_id)
    if result['ok']:
        clases = result['data']
        tema_nuevo = data["temas"].strip().lower()
        fecha_nueva = data["fecha"]
        semana_nueva = int(data["semana"])
        semana_anterior_existe = False
        clases_per_semana = 0

        for clase in clases:
            tema_existente = clase.get("temas", "").strip().lower()
            fecha_existente = clase.get("fecha", "")
            if int(clase.get("semana", 0)) == semana_nueva:
                clases_per_semana += 1
            if int(clase.get("semana", 0)) == semana_nueva - 1:
                semana_anterior_existe = True
            if tema_existente == tema_nuevo:
                flash('Ya existe una clase con ese tema', 'error')
                return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))
            if fecha_existente == fecha_nueva:
                flash('Ya existe una clase con esa fecha', 'error')
                return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))

        if clases_per_semana >= 2:
            flash('No puede haber mas de 2 clases por semana', 'error')
            return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))
        if semana_nueva > 1 and not semana_anterior_existe:
            flash(f'Debe existir una clase en la semana {semana_nueva - 1}.', 'error')
            return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))

    result = post_clase(data)
    flash('Clase creada correctamente.' if result['ok'] else result['description'],
        'success' if result['ok'] else 'error')

    return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))


@courses_bp.route('/cursos/<int:course_id>/clases/<int:id_clase>/editar', methods=['POST'])
def editar_clase(course_id, id_clase):
    if not get_token():
        return redirect(url_for('auth.login'))

    data = {
        "fecha": request.form.get("fecha_clase"),
        "semana": request.form.get("semana"),
        "temas": request.form.get("temas"),
        "tipo": request.form.get("tipo"),
        "modalidad": request.form.get("modalidad"),
        "id_curso": course_id
    }

    if not all([data['fecha'], data['semana'], data['temas'], data['tipo'], data['modalidad']]):
        flash('Falta ingresar datos.', 'error')
        return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))

    result = get_classes_by_course(course_id)
    if result['ok']:
        clases = result['data']
        tema_nuevo = data["temas"].strip().lower()
        fecha_nueva = data["fecha"]
        semana_nueva = int(data["semana"])
        semana_anterior_existe = False
        clases_per_semana = 0

        for clase in clases:
            if clase["id_clase"] == id_clase:
                continue
            tema_existente = clase.get("temas", "").strip().lower()
            fecha_existente = clase.get("fecha", "")
            if int(clase.get("semana", 0)) == semana_nueva:
                clases_per_semana += 1
            if int(clase.get("semana", 0)) == semana_nueva - 1:
                semana_anterior_existe = True
            if tema_existente == tema_nuevo:
                flash('Ya existe una clase con ese tema', 'error')
                return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))
            if fecha_existente == fecha_nueva:
                flash('Ya existe una clase con esa fecha', 'error')
                return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))

        if clases_per_semana >= 2:
            flash('No puede haber mas de 2 clases por semana', 'error')
            return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))
        if semana_nueva > 1 and not semana_anterior_existe:
            flash(f'Debe existir una clase en la semana {semana_nueva - 1}.', 'error')
            return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))

    result = patch_clase(id_clase, data)
    flash('Clase actualizada correctamente.' if result['ok'] else result['description'],
        'success' if result['ok'] else 'error')

    return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))



@courses_bp.route('/cursos/<int:course_id>/clases/<int:id_clase>/eliminar', methods=['POST'])
def eliminar_clase(course_id, id_clase):
    delete_clase(id_clase)
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='calendar'))