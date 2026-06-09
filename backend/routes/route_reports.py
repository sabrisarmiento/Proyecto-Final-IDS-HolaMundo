from flask import Blueprint, request
from services.report_service import (
    report_students_service,
    report_teams_service,
    report_marks_service,
    report_combined_service,
)
from middleware.auth_middleware import require_auth

reports_bp = Blueprint('reports', __name__)

_TRUTHY = {"1", "true", "True", "on", "yes"}


@reports_bp.route("/reportes/alumnos", methods=["GET"])
# @require_auth
def reporte_alumnos():
    return report_students_service(request.args.get("curso_id", type=int))


@reports_bp.route("/reportes/equipos", methods=["GET"])
# @require_auth
def reporte_equipos():
    return report_teams_service(request.args.get("curso_id", type=int))


@reports_bp.route("/reportes/notas", methods=["GET"])
# @require_auth
def reporte_notas():
    curso_id = request.args.get("curso_id", type=int)
    evaluaciones = request.args.getlist("evaluaciones[]") or request.args.getlist("evaluaciones")
    return report_marks_service(curso_id, evaluaciones)


@reports_bp.route("/reportes/exportar", methods=["GET"])
# @require_auth
def reporte_exportar():
    curso_id = request.args.get("curso_id", type=int)
    evaluaciones = request.args.getlist("evaluaciones[]") or request.args.getlist("evaluaciones")
    return report_combined_service(
        curso_id,
        request.args.get("alumnos") in _TRUTHY,
        request.args.get("equipos") in _TRUTHY,
        request.args.get("notas") in _TRUTHY,
        evaluaciones,
    )
