from flask import Blueprint, render_template
from services.material_frontend_service import material_get_all
from services.course_frontend_service import course_get_all

materials_bp = Blueprint('materials', __name__)

SUBJECT = 'Introducción al Desarrollo de Software'

@materials_bp.route('/materiales')
def public_materials():
    materials = material_get_all()
    courses = course_get_all()
    
    chair_by_course = {c['id_curso']: c['catedra'] for c in courses}

    groups = {}

    for material in materials:
        chair = chair_by_course.get(material['id_curso'], 'Sin catedra')
        groups.setdefault(chair, []).append(material)

    sections = [
        {'name': name, 'materials': items}
        for name, items in sorted(groups.items())
    ]

    return render_template(
        "materials.html",
        subject=SUBJECT,
        sections=sections,
        cursos=courses,
        active_page="materials"
    )