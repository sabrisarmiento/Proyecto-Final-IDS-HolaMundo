import hashlib
import os
from flask import jsonify
from helpers.email_sender import send_attendance_email
from helpers.responses import error_response, success_response
from controllers.attendance_controller import (
    get_attendance,
    create_attendance,
    update_attendance,
    delete_attendance,
    active_students_for_class,
    open_attendance_window,
)
from controllers.classes_controller import get_class_id
from helpers.user_belongs import user_can_manage_clase

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:5001")

def attendance_get_handler(id_clase, id_alumno):
    result = get_attendance(id_clase, id_alumno)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "attendance": result["data"]
    })

def attendance_post_handler(data):
    result = create_attendance(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    }, 201)

def attendance_patch_handler(id, data):
    result = update_attendance(id, data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })

def attendance_delete_handler(id):
    result = delete_attendance(id)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })

def send_attendance_link_service(id_clase, horas=None, minutos=None, user=None):
    try:
        if not id_clase:
            return jsonify({"error": "ID de clase no proporcionado"}), 400

        if not user_can_manage_clase(id_clase, user):
            return jsonify({"error": "No tenés permisos sobre esta clase"}), 403

        try:
            horas = int(horas) if horas not in (None, "") else 3
            minutos = int(minutos) if minutos not in (None, "") else 0
        except (ValueError, TypeError):
            return jsonify({"error": "Horas y minutos deben ser numéricos"}), 400

        total_minutos = horas * 60 + minutos
        if total_minutos <= 0 or total_minutos > 24 * 60:
            return jsonify({"error": "La duración debe estar entre 1 minuto y 24 horas"}), 400

        alumnos = active_students_for_class(id_clase)

        if not alumnos:
            return jsonify({"message": "No se encontraron alumnos activos para esta clase"}), 404

        valido_hasta = open_attendance_window(id_clase, total_minutos)
        hora_str = valido_hasta.strftime("%H:%M") if valido_hasta else ""

        context = get_class_id(id_clase)
        clase = context["data"] if context.get("ok") else None

        enviados = 0
        for alumno in alumnos:
            raw_data = f"{alumno['id_alumno']}-{id_clase}-{os.getenv('ATTENDANCE_SECRET')}"
            link_code = hashlib.sha256(raw_data.encode()).hexdigest()

            attendance_link = f"{FRONTEND_URL}/presente?id_alumno={alumno['id_alumno']}&id_clase={id_clase}&code={link_code}"

            if send_attendance_email(alumno['correo'], alumno['nombre'], attendance_link, hora_str, clase):
                enviados += 1

            print(f"Enviando link a {alumno['correo']}: {attendance_link}")

        return jsonify({
            "ok": enviados > 0,
            "message": (
                f"Links de asistencia enviados: {enviados}/{len(alumnos)}."
                if enviados else
                f"No se pudo enviar el link de asistencia a ninguno de los {len(alumnos)} alumnos. Revisá EMAIL_USER/EMAIL_PASS en el .env."
            )
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
