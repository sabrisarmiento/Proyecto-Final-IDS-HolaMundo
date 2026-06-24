from flask import Response
from helpers.responses import error_response
from controllers.reports_controller import report_combined_pdf


def pdf_response(result):
    if not result["ok"]:
        return error_response(result)
    return Response(
        result["data"],
        mimetype="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{result["filename"]}"'
        },
    )


def report_combined_service(opciones):
    return pdf_response(report_combined_pdf(opciones))
