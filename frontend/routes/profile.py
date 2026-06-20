from config import BASE_URL
from flask import Blueprint, request, session
import requests

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/perfil', methods=['POST'])
def update_profile():
  if not session.get('user') or not session.get('token'):
    return {'ok': False, 'message': 'Sesión no válida'}, 401

  user = session['user']
  data = request.get_json(silent=True) or {}
  payload = {
    'nombre': data.get('nombre'),
    'correo': data.get('correo'),
  }

  try:
    response = requests.patch(
      f"{BASE_URL}/users/{user['id_usuario']}",
      json=payload,
      headers={'Authorization': f"Bearer {session['token']}"}
    )

    if response.status_code == 200:
      # Reflejar los cambios en la sesion para que el modal los muestre al recargar.
      user.update(payload)
      session['user'] = user
      return {'ok': True, 'message': 'Perfil actualizado correctamente'}

    body = response.json() if response.content else {}
    errors = body.get('errors') or [{}]
    return {'ok': False, 'message': errors[0].get('description', 'No se pudo actualizar el perfil')}, response.status_code

  except Exception:
    return {'ok': False, 'message': 'Error de conexión con el servidor'}, 502

@profile_bp.route('/perfil/password', methods=['POST'])
def change_password():
  if not session.get('token'):
    return {'ok': False, 'message': 'Sesión no válida'}, 401

  data = request.get_json(silent=True) or {}
  payload = {
    'current_password': data.get('current_password'),
    'new_password': data.get('new_password'),
    'confirm_password': data.get('confirm_password'),
  }

  try:
    response = requests.put(
      f"{BASE_URL}/change-password",
      json=payload,
      headers={'Authorization': f"Bearer {session['token']}"}
    )
    body = response.json() if response.content else {}

    if response.status_code == 200:
      return {'ok': True, 'message': body.get('message', 'Contraseña actualizada correctamente')}

    errors = body.get('errors') or [{}]
    return {'ok': False, 'message': errors[0].get('description', 'No se pudo cambiar la contraseña')}, response.status_code

  except Exception:
    return {'ok': False, 'message': 'Error de conexión con el servidor'}, 502
