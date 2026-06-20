from flask import Blueprint, request
from services.report_service import (
    report_combined_service,
)
from middleware.auth_middleware import require_auth

reports_bp = Blueprint('reports', __name__)

_TRUTHY = {"1", "true", "True", "on", "yes"}


@reports_bp.route("/reportes/exportar", methods=["GET"])
@require_auth
def reporte_exportar():
    curso_id = request.args.get("curso_id", type=int)
    evaluaciones = request.args.getlist("evaluaciones[]") or request.args.getlist("evaluaciones")
    return report_combined_service(
        curso_id,
        request.args.get("alumnos") in _TRUTHY,
        request.args.get("equipos") in _TRUTHY,
        request.args.get("notas") in _TRUTHY,
        evaluaciones,
        request.args.get("asistencia") in _TRUTHY,
        request.args.get("mostrar_corrector") in _TRUTHY,
        request.args.get("incluir_estado_final") in _TRUTHY,
        request.args.get("materia"),
        request.args.get("catedra"),
        request.args.get("cuatrimestre"),
        request.args.get("anio"),
    )
