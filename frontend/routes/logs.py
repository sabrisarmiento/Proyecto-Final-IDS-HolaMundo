import csv
import io
import os
from flask import Blueprint, Response, session, redirect, url_for

logs_bp = Blueprint('logs', __name__)

LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs', 'activity.log')

@logs_bp.route('/logs/descargar')
def descargar_logs():
    if not session.get('user'):
        return redirect(url_for('landing.landing'))

    if not os.path.exists(LOG_PATH):
        return 'No hay logs disponibles', 404

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Fecha y hora', 'Acción', 'Descripción', 'ID Usuario', 'Correo', 'Estado HTTP'])

    with open(LOG_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                writer.writerow(line.split('|'))

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=actividad_usuarios.csv'}
    )