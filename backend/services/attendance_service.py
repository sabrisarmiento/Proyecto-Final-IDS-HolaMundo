import hashlib
from flask import jsonify, request
from helpers.email_sender import send_attendance_email
from controllers.attendance_controller import (
    get_attendance,
    create_attendance,
    update_attendance,
    delete_attendance,
    proximity_fiuba,
    student_active,
    students_active_qr
)

def attendance_get_handler():
    try:
        id_clase = request.args.get("id_clase")
        id_alumno = request.args.get("id_alumno")
        result = get_attendance(id_clase, id_alumno)
        if not result:
            return jsonify({"attendance": []}), 200
        return jsonify({"attendance": result}), 200
    except Exception as error:
        return jsonify({"errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(error)
        }]}), 500

def attendance_post_handler():
    try:
        data = request.get_json()
        
        if not data or "id_alumno" not in data or "id_clase" not in data:
            return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Los campos 'id_alumno' e 'id_clase' son obligatorios"
            }]}), 400
        
        id_alumno = data["id_alumno"]
        lat = data.get("latitud")
        lon = data.get("longitud")

        if not student_active(id_alumno):
            return jsonify({"ok": False, "message": "El alumno figura como abandonó la cursada"}), 403

        if lat is None or lon is None:
            return jsonify({"ok": False, "message": "Se requiere ubicación GPS para validar asistencia"}), 400
        
        if not proximity_fiuba(float(lat), float(lon)):
            return jsonify({"ok": False, "message": "Ubicación fuera del rango permitido"}), 403

        new_id = create_attendance(data)
        return jsonify({"id_asistencia": new_id}), 201
    
    except Exception as error:
        return jsonify({"errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(error)
        }]}), 500

def generate_class_qr_service(id_clase):
    try:
        students = students_active_qr(id_clase)
        
        sent = 0
        for student in students:
            raw_data = f"{student['id_alumno']}-{id_clase}-2026-secret"
            qr_hash = hashlib.sha256(raw_data.encode()).hexdigest()
            
            # URL que captura la ubicación del alumno [cite: 431]
            qr_url = f"https://introds-web.vercel.app/presente?id={student['id_alumno']}&clase={id_clase}&code={qr_hash}"
            
            # Llamada al envío de mail
            if send_attendance_email(student['correo'], student['nombre'], qr_url):
                sent += 1

        return jsonify({
            "ok": True,
            "message": f"Se enviaron {sent} correos con QRs dinámicos."
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def attendance_patch_handler(id):
    try:
        if id <= 0:
            return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El ID debe ser un número entero positivo"
            }]}), 400
        
        data = request.get_json()
        if not data or "presente" not in data:
            return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El campo 'presente' es obligatorio"
            }]}), 400
        
        if not isinstance(data["presente"], bool):
            return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El campo 'presente' debe ser un booleano"
            }]}), 400
        
        if not update_attendance(id, data["presente"]):
            return jsonify({"errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": f"No existe un registro de asistencia con ID {id}"
            }]}), 404
        
        return "", 204
    
    except Exception as error:
        return jsonify({"errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(error)
        }]}), 500

def attendance_delete_handler(id):
    try:
        if id <= 0:
            return jsonify({"errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El ID debe ser un número entero positivo"
            }]}), 400
        
        if not delete_attendance(id):
            return jsonify({"errors": [{
                "code": "404",
                "message": "Not Found",
                "level": "error",
                "description": f"No existe un registro de asistencia con ID {id}"
            }]}), 404
        
        return "", 204
    
    except Exception as error:
        return jsonify({"errors": [{
            "code": "500",
            "message": "Internal Server Error",
            "level": "error",
            "description": str(error)
        }]}), 500

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