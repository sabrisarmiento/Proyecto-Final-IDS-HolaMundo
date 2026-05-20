<<<<<<< Updated upstream
=======
from flask import Blueprint, app, request, jsonify
from database.db import get_connection 
attendance_bp = Blueprint('attendance', __name__)

def update_attendance(id):
        try:
                data = request.get_json()
                estado = data.get('estado')
                
                if estado is None:
                        return jsonify({"error": "Missing 'estado' field"}), 400
        
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE asistencia SET estado = %s WHERE id = %s", (estado, id))
                conn.commit()
        
                if cursor.rowcount == 0:
                        return jsonify({"error": "Attendance record not found"}), 404
        
                return jsonify({"message": "Attendance updated successfully"}), 200
        except Exception as e:
                return jsonify({"error": str(e)}), 500
        finally:
                cursor.close()
                conn.close()

def delete_attendance(id):
        try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM asistencia WHERE id = %s", (id,))
                conn.commit()
        
                if cursor.rowcount == 0:
                        return jsonify({"error": "Attendance record not found"}), 404
        
                return jsonify({"message": "Attendance deleted successfully"}), 200
        except Exception as e:
                return jsonify({"error": str(e)}), 500
        finally:
                cursor.close()
                conn.close()
>>>>>>> Stashed changes
