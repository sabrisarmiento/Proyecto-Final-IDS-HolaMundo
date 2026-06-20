from flask import Response
from helpers.responses import error_response
from controllers.reports_controller import (
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

def report_combined_service(id_curso, incluir_alumnos, incluir_equipos,
                            incluir_notas, evaluaciones,
                            incluir_asistencia=False, mostrar_corrector=False,
                            incluir_estado_final=False):
    return _pdf_response(report_combined_pdf(
        id_curso, incluir_alumnos, incluir_equipos, incluir_notas, evaluaciones,
        incluir_asistencia, mostrar_corrector, incluir_estado_final))
