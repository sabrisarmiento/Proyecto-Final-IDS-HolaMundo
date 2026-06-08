from flask import Blueprint, render_template
from services.attendance_frontend_service import get_all
import requests

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/asistencia')
def attendance():
    asistencia = get_all()
    return render_template("attendance.html", asistencia=asistencia, active_page='attendance')
