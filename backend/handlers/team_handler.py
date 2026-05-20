from flask import jsonify, request

from controller.teams_controller import get_all_teams, team_by_id, get_team_by_members, create_team, update_team, delete_team

def get_teams_handler():
    try:
        response = get_all_teams()
        return jsonify({
            "equipos": response
        }), 200
    except Exception as error:
        return jsonify({
            "errors": [{
                "code": 500,
                "message": "Error al obtener equipos",
                "description": str(error)
            }]
        }), 500

def get_team_by_id_handler(id):
    try:
        response = get_team_by_id(id)
        if not response:
            return jsonify({
                "errors": [{
                    "code": 404,
                    "message": "Equipo no encontrado"
                }]
            }), 404
        return jsonify({
            "equipo": response
        }), 200
    except Exception as error:
        return jsonify({
            "errors": [{
                "code": 500,
                "message": "Error al obtener equipo",
                "description": str(error)
            }]
        }), 500

def get_team_by_members_handler(id_usuario):
    try:
        response = get_team_by_members(id_usuario)
        if not response:
            return jsonify({
                "errors": [{
                    "code": 404,
                    "message": "Equipo no encontrado"
                }]
            }), 404
        return jsonify({
            "equipo": response
        }), 200
    except Exception as error:
        return jsonify({
            "errors": [{
                "code": 500,
                "message": "Error al obtener equipo por integrante",
                "description": str(error)
            }]
        }), 500

def create_team_handler():
    try:
        data = request.get_json()
        nombre_equipo = data.get("nombre_equipo")
        id_creado = create_team(nombre_equipo)
        return jsonify({
            "message": "Equipo creado",
            "id_equipo": id_creado
        }), 201
    except Exception as error:
        return jsonify({
            "errors": [{
                "code": 500,
                "message": "Error al crear equipo",
                "description": str(error)
            }]
        }), 500

def update_team_handler(id):
    try:
        data = request.get_json()
        nombre_equipo = data.get("nombre_equipo")
        update_team(id, nombre_equipo)
        return jsonify({
            "message": "Equipo actualizado"
        }), 200
    except Exception as error:
        return jsonify({
            "errors": [{
                "code": 500,
                "message": "Error al actualizar equipo",
                "description": str(error)
            }]
        }), 500

def delete_team_handler(id):
    try:
        delete_team(id)
        return jsonify({
            "message": "Equipo eliminado"
        }), 200
    except Exception as error:
        return jsonify({
            "errors": [{
                "code": 500,
                "message": "Error al eliminar equipo",
                "description": str(error)
            }]
        }), 500