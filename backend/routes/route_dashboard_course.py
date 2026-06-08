from flask import Blueprint
from services.dashboard_course_service import course_dashboard_service

dashboard_course_bp = Blueprint('dashboard_course', __name__)

@dashboard_course_bp.route('/cursos/<int:id_curso>/dashboard', methods=['GET'])
def get_course_dashboard_route(id_curso):
    return course_dashboard_service(id_curso)