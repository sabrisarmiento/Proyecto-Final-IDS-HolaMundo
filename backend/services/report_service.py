from flask import Response
from helpers.responses import error_response
from controllers.reports_controller import (
    report_students_pdf,
    report_teams_pdf,
    report_marks_pdf,
    report_combined_pdf,
)


def _pdf_response(result):
    if not result["ok"]:
        return error_response(result)
    return Response(
        result["data"],
        mimetype="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{result["filename"]}"'
        },
    )


def report_students_service(id_curso):
    return _pdf_response(report_students_pdf(id_curso))


def report_teams_service(id_curso):
    return _pdf_response(report_teams_pdf(id_curso))


def report_marks_service(id_curso, evaluaciones):
    return _pdf_response(report_marks_pdf(id_curso, evaluaciones))


def report_combined_service(id_curso, incluir_alumnos, incluir_equipos,
                            incluir_notas, evaluaciones):
    return _pdf_response(report_combined_pdf(
        id_curso, incluir_alumnos, incluir_equipos, incluir_notas, evaluaciones))
