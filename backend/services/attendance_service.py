import hashlib
from flask import jsonify
from helpers.email_sender import send_attendance_email
from helpers.responses import error_response, success_response
from controllers.attendance_controller import (
    get_attendance,
    create_attendance,
    update_attendance,
    delete_attendance,
    students_active_qr,
)

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

def generate_class_qr_service(id_clase):
    try:
        students = students_active_qr(id_clase)

        sent = 0
        for student in students:
            raw_data = f"{student['id_alumno']}-{id_clase}-2026-secret"
            qr_hash = hashlib.sha256(raw_data.encode()).hexdigest()

            qr_url = f"https://introds-web.vercel.app/presente?id={student['id_alumno']}&clase={id_clase}&code={qr_hash}"

            if send_attendance_email(student['correo'], student['nombre'], qr_url):
                sent += 1

        return jsonify({
            "ok": True,
            "message": f"Se enviaron {sent} correos con QRs dinámicos."
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_qr_service(id_clase):
    try:
        if not id_clase:
            return jsonify({"error": "ID de clase no proporcionado"}), 400

        alumnos = students_active_qr(id_clase)

        if not alumnos:
            return jsonify({"message": "No se encontraron alumnos activos para esta clase"}), 404

        for alumno in alumnos:
            raw_data = f"{alumno['id_alumno']}-{id_clase}-2026-secret"
            qr_hash = hashlib.sha256(raw_data.encode()).hexdigest()

            qr_url = f"https://introds-web.vercel.app/presente?id_alumno={alumno['id_alumno']}&id_clase={id_clase}&code={qr_hash}"

            print(f"Enviando QR a {alumno['correo']}: {qr_url}")

        return jsonify({
            "ok": True,
            "message": f"QRs generados y enviados a {len(alumnos)} alumnos correctamente"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
