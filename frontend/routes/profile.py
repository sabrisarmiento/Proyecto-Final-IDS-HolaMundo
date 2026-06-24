from flask import Blueprint, request, session, redirect, flash
from services.users_service import patch_user2, put_password_user

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

  result = patch_user2(user['id_usuario'], payload)

  if result['ok']:
    user.update(payload)
    session['user'] = user
    flash('Perfil actualizado correctamente', 'perfil_ok')
  else:
    flash(result['description'], 'perfil_error')

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

  result = put_password_user(payload)

  if result['ok']:
    flash(result['message'], 'password_ok')
    return redirect(next_page + '?open=perfil')
  
  flash(result['description'], 'password_error')
  return redirect(next_page + '?open=perfil&pane=password')
