from urllib.parse import urlsplit, urlunsplit
from flask import Blueprint, request, redirect, url_for, session
import requests

profile_bp = Blueprint('profile', __name__)

def _redirect_back(status):
  """Vuelve a la pagina anterior agregando ?perfil=<status> (descartando
  cualquier query previa para no acumular flags)."""
  back = request.referrer or url_for('dashboard.dashboard')
  scheme, netloc, path, _query, fragment = urlsplit(back)
  return redirect(urlunsplit((scheme, netloc, path, f'perfil={status}', fragment)))

@profile_bp.route('/perfil', methods=['POST'])
def update_profile():
  if not session.get('user') or not session.get('token'):
    return redirect(url_for('landing.landing'))

  user = session['user']
  payload = {
    'nombre': request.form.get('nombre'),
    'correo': request.form.get('correo'),
  }

  try:
    response = requests.patch(
      f"http://127.0.0.1:5000/users/{user['id_usuario']}",
      json=payload,
      headers={'Authorization': f"Bearer {session['token']}"}
    )

    if response.status_code == 200:
      # Reflejar los cambios en la sesion para que el modal los muestre al recargar.
      user.update(payload)
      session['user'] = user
      return _redirect_back('ok')

    return _redirect_back('error')

  except Exception:
    return _redirect_back('error')

@profile_bp.route('/perfil/password', methods=['POST'])
def change_password():
  """Cambio de contrasena via AJAX. Reenvia el PUT /change-password al backend
  con el token de la sesion y devuelve JSON para que el front lo muestre inline."""
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
      'http://127.0.0.1:5000/change-password',
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
