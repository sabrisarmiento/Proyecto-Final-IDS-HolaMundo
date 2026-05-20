from flask import Blueprint, jsonify,request
from controller.exam_controller import get_exams, get_exam_via_id, update_exam_via_id
from database.db import modify_db, query_db

exam_bp = Blueprint('exam', __name__)

#GET GENERAL y GET TIPO Y FECHA------------------------------
@exam_bp.route("/evaluaciones", methods=["GET"])
def obtain_exams_params():
    type = request.args.get("id_tipo")
    date = request.args.get("fecha")

    return get_exams(type, date)

#GET ID------------------------------------------------------
@exam_bp.route("/examenes/<int:id>",methods=["GET"])
def obtain_exam_id(id):
    return get_exam_via_id(id)

#POST--------------------------------------------------------
@exam_bp.route("/examenes", methods=["POST"]) 
def add_exam():
    data = request.get_json()

    if not data:
        return jsonify({ "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "No se completaron los datos"
            }]}), 400
    
    id_tipo = data.get("id_tipo")
    id_profesor = data.get("id_profesor")
    id_equipo = data.get("id_equipo ")
    fecha = data.get("fecha")

    if not id_tipo or not fecha or not id_profesor or not id_equipo:
        return jsonify({ "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "Falta un campo obligatorio"
            }]}), 400
    
    try:
        query = "INSERT INTO evaluaciones (id_tipo, id_profesor, id_equipo, fecha) VALUES (%s, %s, %s, %s)"
        params = (id_tipo, id_profesor, id_equipo, fecha)
        new_id = modify_db(query, params)

        return jsonify({"id": new_id}), 201

    except Exception as error:
        return jsonify({ "errors": [{
                "code": "500",
                "message": "Internal Server Error",
                "level": "error",
                "description": str(error)
            }]}), 500
    
#PATCH ID----------------------------------------------------
@exam_bp.route("/examenes/<int:id>", methods=["PATCH"])
def modify_exam(id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({ "errors": [{
                "code": "400", 
                "message": "Bad Request", 
                "level": "error", 
                "description": "Debe enviar al menos un campo para actualizar"
            }]}), 400
        
        campos_validos = ["id_tipo", "id_profesor", "id_equipo", "fecha"]
        for campo in data:
            if campo not in campos_validos:
                return jsonify({ "errors": [{
                    "code": "400", 
                    "message": "Bad Request", 
                    "level": "error", 
                    "description": f"El campo '{campo}' no es válido"
                }]}), 400

        resultado = update_exam_via_id(id, data)

        if not resultado:
            return jsonify({ "errors": [{
                "code": "404", 
                "message": "No encontrado", 
                "level": "error", 
                "description": f"No existe el examen con id: {id}"
            }]}), 404
        
        return '', 204
    
    except Exception as error:
        return jsonify({ "errors": [{
            "code": "500", 
            "message": "Internal Server Error", 
            "level": "error", 
            "description": str(error)
        }]}), 500




#DELETE ID---------------------------------------------------
@exam_bp.route("/examenes/<int:id>", methods=["DELETE"])
def delete_exam(id):
    if id <= 0:
        return jsonify({ "errors": [{
                "code": "400",
                "message": "Bad Request",
                "level": "error",
                "description": "El ID debe ser un número entero positivo mayor a cero."
            }]}), 400

    try:

        exam = query_db("SELECT id FROM evaluaciones WHERE id = %s", (id,))

        if not exam:
            return jsonify({ "errors": [{
                    "code": "404",
                    "message": "Not Found",
                    "level": "error",
                    "description": "No existe una evaluacion con el ID proporcionado."
                }]}), 404

        modify_db("DELETE FROM evaluaciones WHERE id = %s", (id,))

        return '', 204
    
    except Exception as e:
        return jsonify({ "errors": [{
                "code": "500",
                "message": "Internal Server Error",
                "level": "error",
                "description": str(e)
            }]}), 500
