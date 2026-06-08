from flask import Blueprint, render_template, request
from services.material_frontend_service import material_get_all
from services.subjects_service import get_subjects
from services.courses_service import get_courses

materials_bp = Blueprint('materials', __name__)

SUBJECT = 'Introducción al Desarrollo de Software'

@materials_bp.route('/materiales')
def public_materials():
    subject_id = request.args.get('subject')
    course_id = request.args.get('curso')
    
    subjects = get_subjects()
    courses = []
    sections = []

    if subject_id:
        selected_subject = next((s for s in subjects if str(s["id_materia"]) == subject_id), None)
        subject_name = selected_subject.get("nombre") if selected_subject else None
        courses = [c for c in get_courses() if c.get("materia") == subject_name]

    if course_id:
        materials = [m for m in material_get_all() if str(m.get("id_curso")) == course_id]
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
        active_page="materials",
        subjects=subjects,
        courses=courses,
        sections=sections,
        subject_id=subject_id,
        course_id=course_id,
    )