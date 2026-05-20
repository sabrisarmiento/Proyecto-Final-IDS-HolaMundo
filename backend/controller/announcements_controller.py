from flask import Blueprint, request, jsonify
from database.db import get_connection 
announcements_bp = Blueprint('announcements', __name__)

def  get_announcements():
        try:
                fecha = request.args.get('fecha')
                titulo = request.args.get('titulo')
        
                query = "SELECT * FROM avisos WHERE 1=1"
                params = []
        
                if fecha:
                        query += " AND fecha = %s"
                        params.append(fecha)
                
                if titulo:
                        query += " AND titulo = %s"
                        params.append(titulo)
                

                query += " ORDER BY fecha DESC"
        
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query, params)
                announcements = cursor.fetchall()
                
                return jsonify(announcements), 200
        except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        finally:                
                cursor.close()
                conn.close()

def get_announcement_by_id(id):
        try:
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM avisos WHERE id_aviso = %s", (id,))
                announcement = cursor.fetchone()
        
                if not announcement:
                        return jsonify({"error": "Announcement not found"}), 404
                
                return jsonify(announcement), 200
        except Exception as e:
                return jsonify({"error": str(e)}), 500
        finally:
                cursor.close()
                conn.close()

def create_announcement():
        try:
                data = request.get_json()
                titulo = data.get('titulo')
                descripcion = data.get('descripcion')
                fecha = data.get('fecha')
        
                if not titulo or not descripcion or not fecha:
                        return jsonify({"error": "Missing required fields"}), 400
        
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO avisos (titulo, descripcion, fecha) VALUES (%s, %s, %s)", (titulo, descripcion, fecha))
                conn.commit()
        
                return jsonify({"message": "Announcement created successfully"}), 201
        except Exception as e:
                return jsonify({"error": str(e)}), 500
        finally:
                cursor.close()
                conn.close()
                

def update_announcement(id):
        try:
                data = request.get_json()
                
                campos = []
                params = []
                
                if 'titulo' in data:
                        campos.append("titulo = %s")
                        params.append(data['titulo'])
                if 'mensaje' in data:
                        campos.append("descripcion = %s")
                        params.append(data['descripcion'])
                if 'fecha' in data:
                        campos.append("fecha = %s")
                        params.append(data['fecha'])
                if not campos:
                        return jsonify({"error": "No fields to update"}), 400
                        
                params.append(id)
                query = f"UPDATE avisos SET {', '.join(campos)} WHERE id = %s"
                
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                
                if cursor.rowcount == 0:
                        return jsonify({"error": "Announcement not found"}), 404
                
                return jsonify({"message": "Announcement updated successfully"}), 200
        except Exception as e:
                return jsonify({"error": str(e)}), 500
        finally:
                cursor.close()
                conn.close()

def delete_announcement(id):
        try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM avisos WHERE id = %s", (id,))
                conn.commit()
        
                if cursor.rowcount == 0:
                        return jsonify({"error": "Announcement not found"}), 404
                
                return jsonify({"message": "Announcement deleted successfully"}), 200
        except Exception as e:
                return jsonify({"error": str(e)}), 500
        finally:
                cursor.close()
                conn.close()