from flask import Blueprint, render_template, session, request, redirect, url_for
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
      course = course_res.json().get("course") or {}
  except:
      course = {}

  try:
      token = session.get('token')
      headers = {'Authorization': f'Bearer {token}'}
      students_res = requests.get(
        f'http://127.0.0.1:5000/students?id_curso={course_id}&page={page}&per_page={per_page}'
        + (f"&order_by={order_by}" if order_by else "")
        + (f"&order={order}" if order else ""),
        headers=headers
      )
      response_data = students_res.json()
      students_data = response_data.get("students") or []
      total = response_data.get("total") or 0
  except Exception as e:
      students_data = []
      total = 0

  total_pages = max(1, (total + per_page - 1) // per_page)


  return render_template('course_detail.html', course=course, students=students_data, active_page='courses', page=page, total_pages=total_pages, course_id=course_id, active_tab=active_tab)