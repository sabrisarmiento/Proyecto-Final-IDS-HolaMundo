from flask import Blueprint, request, redirect, url_for, session
from services.users_service import login_user

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
  correo = request.form.get('correo')
  contraseña = request.form.get('contraseña')

  result = login_user(correo, contraseña)

  if result['ok']:
    session['token'] = result['token']
    session['user'] = result['user']
    return redirect(url_for('dashboard.dashboard'))

  return redirect(url_for('landing.landing') + f'?error={result["description"]}')


@login_bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('landing.landing'))