from flask import Blueprint, render_template, session
from services.material_frontend_service import MaterialFrontendService
from services.course_frontend_service import CourseFrontendService

materials_bp = Blueprint('materials', __name__)

@materials_bp.route('/materiales')
def public_materials():
    id_curso = session.get("selected_course", 1)
    materiales_api = MaterialFrontendService.get_all(id_curso)
    cursos = CourseFrontendService.get_all()
    return render_template(
        "materials.html",
        materiales=materiales_api,
        cursos=cursos,
        selected_course=id_curso,
        active_page="materials"
    )
