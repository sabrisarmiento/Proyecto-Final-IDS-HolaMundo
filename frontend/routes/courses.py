from flask import Blueprint, render_template
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

  return render_template('courses.html', courses=courses)