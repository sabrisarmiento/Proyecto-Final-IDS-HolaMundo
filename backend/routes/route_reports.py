from flask import Blueprint, request
from services.report_service import report_combined_service
from middleware.auth_middleware import require_auth

reports_bp = Blueprint('reports', __name__)


def bool_arg(name):
    return request.args.get(name) in {"true", "True", "1"}

@reports_bp.route("/reportes/exportar", methods=["GET"])
@require_auth
def reporte_exportar():
    opciones = {
        "id_curso":             request.args.get("curso_id", type=int),
        "incluir_alumnos":      bool_arg("alumnos"),
        "incluir_equipos":      bool_arg("equipos"),
        "incluir_notas":        bool_arg("notas"),
        "evaluaciones":         request.args.getlist("evaluaciones[]") or request.args.getlist("evaluaciones"),
        "incluir_asistencia":   bool_arg("asistencia"),
        "mostrar_corrector":    bool_arg("mostrar_corrector"),
        "incluir_estado_final": bool_arg("incluir_estado_final"),
        "materia":              request.args.get("materia"),
        "catedra":              request.args.get("catedra"),
        "cuatrimestre":         request.args.get("cuatrimestre"),
        "anio":                 request.args.get("anio"),
    }
    return report_combined_service(opciones)
