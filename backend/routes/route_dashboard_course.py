from flask import Blueprint
from services.dashboard_course_service import course_dashboard_service
from middleware.auth_middleware import require_auth

dashboard_course_bp = Blueprint('dashboard_course', __name__)

@dashboard_course_bp.route('/cursos/<int:id_curso>/dashboard', methods=['GET'])
@require_auth
def get_course_dashboard_route(id_curso):
    return course_dashboard_service(id_curso)