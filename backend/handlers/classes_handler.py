from flask import jsonify, request
from controller.classes_controller import get_classes, get_class_id, create_class, update_class

def classes_get_handler():
    try:
        date = request.args.get('fecha')
        response = get_classes(date)

        if not response:
            return jsonify({"classes": []}), 204

        return jsonify({"classes": response}), 200

    except Exception as error:
        return jsonify({"errors": [{"code": "500","message": "Internal Server Error","level": "error","description": str(error)}]}), 500

def class_get_handler(id):
    try:
        if id <= 0:
            return jsonify({ "errors": [{"code": "400","message": "Bad Request","level": "error","description": "El ID debe ser un número entero positivo"}]}), 400

        response = get_class_id(id)

        if not response:
            return jsonify({ "errors": [{"code": "404","message": "Not Found","level": "error","description": f"No se encontró la clase con ID {id}"}]}), 404

        return jsonify({"class": response}), 200

    except Exception as error:
        return jsonify({"errors": [{"code": "500","message": f"Error al obtener la clase con ID {id}","level": "error","description": str(error)}]}), 500

def class_post_handler():
    try:
        data = request.get_json()
        
        if not data or 'date' not in data or 'course_id' not in data:
            return jsonify({ "errors": [{"code": "400", "message": "Bad Request", "level": "error", "description": "Faltan campos obligatorios (date, course_id)"}]}), 400

        new_id = create_class(data)
        return jsonify({"message": "Class created successfully", "class_id": new_id}), 201

    except Exception as error:
        return jsonify({"errors": [{"code": "500","message": "Internal Server Error","level": "error","description": str(error)}]}), 500

def class_patch_handler(id):
    try:
        if id <= 0:
            return jsonify({ "errors": [{"code": "400","message": "Bad Request","level": "error","description": "El ID debe ser un número entero positivo"}]}), 400

        data = request.get_json()
        if not data:
            return jsonify({ "errors": [{"code": "400","message": "Bad Request","level": "error","description": "No se enviaron datos para actualizar"}]}), 400

        updated = update_class(id, data)
        
        if not updated:
            return jsonify({ "errors": [{"code": "404","message": "Not Found","level": "error","description": f"No se pudo actualizar o no existe la clase con ID {id}"}]}), 404

        return jsonify({"message": "Class updated successfully"}), 200

    except Exception as error:
        return jsonify({"errors": [{"code": "500","message": f"Error al actualizar la clase con ID {id}","level": "error","description": str(error)}]}), 500