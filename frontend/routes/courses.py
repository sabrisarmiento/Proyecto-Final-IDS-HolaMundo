from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests
 
courses_bp = Blueprint('courses', __name__)

#Cursos (todos)

@courses_bp.route('/cursos')
def courses():
  try:
    response = requests.get('http://127.0.0.1:5000/courses')
    data = response.json()
    courses = data.get("courses") or data.get("data") or []
  except Exception as e:
    courses = []
  return render_template('courses.html', courses=courses, active_page='courses')

#Detalle del curso

@courses_bp.route('/cursos/<int:course_id>', methods=['GET', 'POST'])
def course_detail(course_id):
  if request.method == 'POST':
    try:
      token = session.get('token')
      headers = {'Authorization': f'Bearer {token}'}
      data = {
        "nombre": request.form.get('nombre'),
        "apellido": request.form.get('apellido'),
        "padron": int(request.form.get('padron')),
        "correo": request.form.get('correo'),
        "id_curso": course_id
        }
      requests.post('http://127.0.0.1:5000/students', headers=headers, json=data)
    except Exception as e:
      print(f"Error creating student: {e}")
    return redirect(url_for('courses.course_detail', course_id=course_id, tab='students'))
    
  active_tab = request.args.get('tab', 'general')
  page = request.args.get('page', 1, type=int)
  per_page = 10
  order_by = request.args.get('order_by')
  order = request.args.get('order')

  try:
      course_res = requests.get(f'http://127.0.0.1:5000/courses/{course_id}')
      course_json = course_res.json()
      course = (
        course_json.get("course")
        or course_json.get("data")
        or course_json.get("curso")
        or {}
      )
  except:
      course = {}
      
  try:
    evals_res = requests.get(
      f'http://127.0.0.1:5000/evaluaciones?id_curso={course_id}',
      headers=headers
    )
    evals_json = evals_res.json()
    evaluaciones = (
      evals_json.get("evaluaciones")
      or evals_json.get("exams")
      or []
    )
  except Exception as e:
    evaluaciones = []

  try:
      token = session.get('token')
      headers = {'Authorization': f'Bearer {token}'}
      students_res = requests.get(
        f'http://127.0.0.1:5000/students?id_curso={course_id}'
        + (f'&page={page}&per_page={per_page}')
        + (f"&order_by={order_by}" if order_by else "")
        + (f"&order={order}" if order else ""),
        headers=headers
      )
      response_data = students_res.json()
      students_data = (
        response_data.get("data")
        or response_data.get("students")
        or response_data.get("alumnos")
        or []
      )
      total = response_data.get("total") or 0
  except Exception as e:
      students_data = []
      total = 0

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
 
  eval_id_sel = session.get('eval_seleccionada')
  eval_seleccionada = next(
    (e for e in evaluaciones if e['id_evaluacion'] == eval_id_sel),
    None
  )
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
  promedio_general = round(
    sum(todos_los_valores) / len(todos_los_valores), 1
  ) if todos_los_valores else 0.0

  total_pages = max(1, (total + per_page - 1) // per_page)

  return render_template(
    'course_detail.html',
    course=course,
    students=students_data,
    active_page='courses',
    page=page,
    total_pages=total_pages,
    course_id=course_id,
    active_tab=active_tab,
    #order_by=order_by,
    #order=order,
    evaluaciones=evaluaciones,
    eval_seleccionada=eval_seleccionada,
    promedio_eval=promedio_eval,
    promedio_general=promedio_general,
  )

#@courses_bp.route('/cursos/<int:course_id>')
#def course_detail(course_id):
#    token = session.get('token')
#    headers = {'Authorization': f'Bearer {token}'}
# 
#    try:
#        res_course = requests.get(f'http://127.0.0.1:5000/courses/{course_id}', headers=headers)
#        if res_course.status_code != 200:
#            flash("No se pudo encontrar el curso")
#            return redirect(url_for('dashboard.dashboard'))
# 
#        course_json = res_course.json()
#        course = (
#            course_json.get("course")
#            or course_json.get("data")
#            or course_json.get("curso")
#        )
# 
#        res_evals = requests.get(
#            f'http://127.0.0.1:5000/evaluaciones?id_curso={course_id}',
#            headers=headers
#        )
#        evaluaciones = []
#        if res_evals.status_code == 200:
#            evaluaciones = res_evals.json().get("evaluaciones", []) or res_evals.json().get("exams", []) or []
# 
#        res_students = requests.get(
#            f'http://127.0.0.1:5000/students_with_notes?id_curso={course_id}',
#            headers=headers
#        )
#        students_raw = []
# 
#        if res_students.status_code == 200:
#            try:
#                data_json = res_students.json()
#                students_raw = (
#                    data_json.get("data")
#                    or data_json.get("students")
#                    or data_json.get("alumnos")
#                    or []
#                )
#            except Exception:
#                print("Error: JSON de alumnos")
# 
#        for s in students_raw:
#            notas_dict = {}
#            raw_string = s.get('notas_raw') or ""
#            if raw_string:
#                for par in raw_string.split(','):
#                    if ':' in par:
#                        id_ev, nota = par.split(':', 1)
#                        try:
#                            notas_dict[int(id_ev.strip())] = nota.strip()
#                        except ValueError:
#                            pass
#            s['notas_todas'] = notas_dict
# 
#            if not s.get('promedio_final') and notas_dict:
#                valores = [float(v) for v in notas_dict.values() if v not in ('', None)]
#                s['promedio_final'] = round(sum(valores) / len(valores), 1) if valores else None
# 
#        for s in students_raw:
#            notas_dict = {}
#            raw_string = s.get('notas_raw') or ""
#            if raw_string:
#                for par in raw_string.split(','):
#                    if ':' in par:
#                        id_ev, nota = par.split(':', 1)
#                        try:
#                            notas_dict[int(id_ev.strip())] = nota.strip()
#                        except ValueError:
#                            pass
#            s['notas_todas'] = notas_dict
#
#            correctores_dict = {}
#            raw_corr = s.get('correctores_raw') or ""
#            if raw_corr:
#                for par in raw_corr.split(','):
#                    if ':' in par:
#                        id_ev, nombre_corr = par.split(':', 1)
#                        try:
#                            val = nombre_corr.strip()
#                            if val:
#                                correctores_dict[int(id_ev.strip())] = val
#                        except ValueError:
#                            pass
#            s['correctores_todas'] = correctores_dict
#
#            if not s.get('promedio_final') and notas_dict:
#                valores = [float(v) for v in notas_dict.values() if v not in ('', None)]
#                s['promedio_final'] = round(sum(valores) / len(valores), 1) if valores else None
#
#        eval_id_sel = session.get('eval_seleccionada')
#        eval_seleccionada = next(
#            (e for e in evaluaciones if e['id_evaluacion'] == eval_id_sel),
#            None
#        )
#        if not eval_seleccionada and evaluaciones:
#            eval_seleccionada = evaluaciones[0]
# 
#        promedio_eval = 0.0
#        if eval_seleccionada:
#            notas_activa = []
#            for s in students_raw:
#                n = s.get('notas_todas', {}).get(eval_seleccionada['id_evaluacion'])
#                if n not in (None, ''):
#                    try:
#                        notas_activa.append(float(n))
#                    except ValueError:
#                        pass
#            promedio_eval = round(sum(notas_activa) / len(notas_activa), 1) if notas_activa else 0.0
# 
#        todos_los_valores = []
#        for s in students_raw:
#            for nota in (s.get('notas_todas') or {}).values():
#                if nota not in (None, ''):
#                    try:
#                        todos_los_valores.append(float(nota))
#                    except ValueError:
#                        pass
#        promedio_general = round(
#            sum(todos_los_valores) / len(todos_los_valores), 1
#        ) if todos_los_valores else 0.0
# 
#        return render_template(
#            'course_detail.html',
#            course=course,
#            students=students_raw,
#            evaluaciones=evaluaciones,
#            eval_seleccionada=eval_seleccionada,
#            promedio_eval=promedio_eval,
#            promedio_general=promedio_general,
#        )
# 
#    except Exception as e:
#        print(f"Error crítico en course_detail: {e}")
#        flash("Ocurrió un error al cargar el detalle")
#        return redirect(url_for('dashboard.dashboard'))
 

@courses_bp.route('/cambiar-evaluacion', methods=['POST'])
def cambiar_evaluacion():
    eval_id = request.form.get('eval_activa')
    if eval_id:
        session['eval_seleccionada'] = int(eval_id)
 
    referrer = request.referrer or '/cursos'
    base_url = referrer.split('#')[0]
    return redirect(base_url + '#tab-ads')
 
 
@courses_bp.route('/cursos/<int:course_id>/notas/guardar', methods=['POST'])
def guardar_notas(course_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('auth.login'))
 
    headers = {'Authorization': f'Bearer {token}'}
    id_eval = request.form.get('id_evaluacion')
 
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
        json={
            'id_evaluacion': id_eval,
            'notas': notas_dict,
            'correctores': correctores_dict,
        },
        headers=headers
    )
 
    return redirect(f'/cursos/{course_id}#tab-ads')
 
 
@courses_bp.route('/cursos/<int:course_id>/evaluaciones/crear', methods=['POST'])
def crear_evaluacion(course_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('auth.login'))
 
    nombre = request.form.get('nombre_eval')
    headers = {'Authorization': f'Bearer {token}'}
 
    requests.post(
        'http://127.0.0.1:5000/evaluaciones',
        json={'id_curso': course_id, 'id_tipo': 1, 'nombre': nombre},
        headers=headers
    )
 
    session.pop('eval_seleccionada', None)
 
    return redirect(f'/cursos/{course_id}#tab-ads')
 
 
@courses_bp.route('/cursos/<int:course_id>/evaluaciones/eliminar/<int:eval_id>', methods=['POST'])
def eliminar_evaluacion(course_id, eval_id):
    token = session.get('token')
    if not token:
        return redirect(url_for('auth.login'))
 
    headers = {'Authorization': f'Bearer {token}'}
 
    requests.delete(
        f'http://127.0.0.1:5000/evaluaciones/{eval_id}',
        headers=headers
    )
 
    if session.get('eval_seleccionada') == eval_id:
        session.pop('eval_seleccionada', None)
 
    return redirect(f'/cursos/{course_id}#tab-ads')
