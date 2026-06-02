from flask import Blueprint, render_template, session, redirect, request
import requests

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/cursos')
def courses():
  try:
    response = requests.get('http://127.0.0.1:5000/courses')
    data = response.json()
    courses = data.get("courses") or data.get("data") or []
  except Exception as e:
    courses = []
  return render_template('courses.html', courses=courses, active_page='courses')

@courses_bp.route('/set-course/<int:course_id>')
def set_course(course_id):

    session['selected_course'] = course_id

    next_page = request.args.get('next')

    if next_page:
        return redirect(next_page)

    return redirect('/')

# DETALLE DE CURSO

@courses_bp.route('/cursos/<int:course_id>')
def course_detail(course_id):
  try:
    course_res = requests.get(f'http://127.0.0.1:5000/courses/{course_id}')
    data = course_res.json()
    course = data.get("course") or data.get("data") or {}
  except Exception as e:
    course = {}

  try:
    token = session.get('token')
    headers = {'Authorization': f'Bearer {token}'}
    students_res = requests.get(f'http://127.0.0.1:5000/students?id_curso={course_id}', headers=headers)
    students_data = students_res.json().get("students") or []
  except:
    students_data = []

  return render_template('course_detail.html', course=course, active_page='courses', students=students_data)