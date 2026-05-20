from flask import Blueprint
<<<<<<< Updated upstream

attendance_bp = Blueprint('attendance', __name__)
=======
attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/attendance/<id>', methods=['PATCH'])
def update_attendance(id):
        return f"Modificar asistencia para ID: {id}"
    
@attendance_bp.route('/attendance/<id>', methods=['DELETE'])
def delete_attendance(id):
        return f"Eliminar asistencia para ID: {id}"
>>>>>>> Stashed changes
