from flask import Blueprint, render_template
from services.material_frontend_service import MaterialFrontendService
from services.course_frontend_service import CourseFrontendService

materials_bp = Blueprint('materials', __name__)

SUBJECT = 'Introducción al Desarrollo de Software'

@materials_bp.route('/materiales')
def public_materials():
    materials = MaterialFrontendService.get_all()
    courses = CourseFrontendService.get_all()
    
    chair_by_course = {c['id_curso']: c['catedra'] for c in courses}

    groups = {}

    for material in materials:
        chair = chair_by_course.get(material['id_curso'], 'Sin catedra')
        groups.setdefault(chair, []).append(material)

    sections = [
        {'name': name, 'materials': items}
        for name, items in sorted(groups.items())
    ]

    return render_template("materials.html", subject=SUBJECT, sections=sections)
