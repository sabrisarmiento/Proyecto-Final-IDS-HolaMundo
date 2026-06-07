from flask import Blueprint, request
from services.exam_service import (
    exams_service,
    exam_service,
    create_exam_service,
    patch_exam_service,
    delete_exam_service,
    save_exam_notes_service,
    students_notes_report_service,
    get_promocion_config_service,
    save_promocion_config_service,
)
from middleware.auth_middleware import require_auth
from helpers.logger import log_action
 
exam_bp = Blueprint('exam', __name__)

@exam_bp.route("/evaluaciones", methods=["GET"])
def obtain_exams_params():
    filters = {
        "id_tipo":    request.args.get('id_tipo'),
        "id_usuario": request.args.get('id_usuario'),
        "fecha":      request.args.get('fecha'),
        "id_curso":   request.args.get('id_curso')
    }
    return exams_service(filters)
 
 
@exam_bp.route("/evaluaciones", methods=["POST"])
# @require_auth # descomentar cuando el auth este listo
def add_exam():
    data = request.get_json()
    return create_exam_service(data)
 
 
@exam_bp.route("/evaluaciones/<int:id>", methods=["GET"])
def obtain_exam_id(id):
    return exam_service(id)
 
 
@exam_bp.route("/evaluaciones/<int:id>", methods=["PATCH"])
@require_auth
def modify_exam(id):
    data = request.get_json()
    return patch_exam_service(id, data)
 
 
@exam_bp.route("/evaluaciones/<int:id>", methods=["DELETE"])
# @require_auth # descomentar cuando el auth este listo
def delete_exam(id):
    return delete_exam_service(id)
 
 
@exam_bp.route("/notas/guardar", methods=["POST"])
# @require_auth  # descomentar cuando el auth este listo
def save_notes():
    data = request.get_json()
    id_exam = data.get('id_evaluacion')
    notes = data.get('notas', {})
    correctores = data.get('correctores', {})
    
    id_corrector = None
    if hasattr(request, 'user') and request.user:
        id_corrector = request.user.get('id_usuario')

    result = save_exam_notes_service(id_exam, notes, id_corrector, correctores)

    if result[1] == 200:
        nombre_u = ""
        if hasattr(request, "user") and request.user:
            nombre_u = f"{request.user.get('nombre','')} {request.user.get('apellido','')}".strip() or request.user.get("correo", "")
        log_action(
            accion="GUARDAR_NOTAS",
            descripcion=f"Se guardaron notas de la evaluación ID {id_exam} ({len(notes)} alumnos)",
            id_usuario=id_corrector,
            nombre_usuario=nombre_u,
            id_curso=int(data.get("id_curso", 0)) or None,
        )

    return result
 
@exam_bp.route("/students_with_notes", methods=["GET"])
def obtain_students_report():
    id_curso = request.args.get('id_curso')
    return students_notes_report_service(id_curso)

# PROMOCIÓN

@exam_bp.route("/cursos/<int:id_curso>/promocion", methods=["GET"])
def get_promocion_config(id_curso):
    return get_promocion_config_service(id_curso)


@exam_bp.route("/cursos/<int:id_curso>/promocion", methods=["POST"])
# @require_auth # descomentar cuando el auth este listo
def save_promocion_config(id_curso):
    return save_promocion_config_service(id_curso, request.get_json(silent=True))