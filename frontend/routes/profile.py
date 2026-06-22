from config import BASE_URL
from flask import Blueprint, request, session, redirect, flash
import requests

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/perfil', methods=['POST'])
def update_profile():
  if not session.get('user') or not session.get('token'):
    return redirect('/')

  next_page = request.form.get('next', '/')
  user = session['user']
  payload = {
    'nombre': request.form.get('nombre'),
    'correo': request.form.get('correo'),
  }

  try:
    response = requests.patch(
      f"{BASE_URL}/users/{user['id_usuario']}",
      json=payload,
      headers={'Authorization': f"Bearer {session['token']}"}
    )

    if response.status_code == 200:
      user.update(payload)
      session['user'] = user
      flash('Perfil actualizado correctamente', 'perfil_ok')
    else:
      body = response.json() if response.content else {}
      errors = body.get('errors') or [{}]
      flash(errors[0].get('description', 'No se pudo actualizar el perfil'), 'perfil_error')

  except Exception:
    flash('Error de conexión con el servidor', 'perfil_error')

  return redirect(next_page + '?open=perfil')


@profile_bp.route('/perfil/password', methods=['POST'])
def change_password():
  if not session.get('token'):
    return redirect('/')

  next_page = request.form.get('next', '/')
  payload = {
    'current_password': request.form.get('current_password'),
    'new_password': request.form.get('new_password'),
    'confirm_password': request.form.get('confirm_password'),
  }

  try:
    response = requests.put(
      f"{BASE_URL}/change-password",
      json=payload,
      headers={'Authorization': f"Bearer {session['token']}"}
    )
    body = response.json() if response.content else {}

    if response.status_code == 200:
      flash(body.get('message', 'Contraseña actualizada correctamente'), 'password_ok')
      return redirect(next_page + '?open=perfil')

    errors = body.get('errors') or [{}]
    flash(errors[0].get('description', 'No se pudo cambiar la contraseña'), 'password_error')

  except Exception:
    flash('Error de conexión con el servidor', 'password_error')

  return redirect(next_page + '?open=perfil&pane=password')
