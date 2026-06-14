from flask import Blueprint, request, redirect, url_for, session
import requests

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
  correo = request.form.get('correo')
  contraseña = request.form.get('contraseña')

  try:
    response = requests.post('http://127.0.0.1:5000/login', json={  # requests (librería)
      "correo": correo,
      "contraseña": contraseña
    })
    print("STATUS:", response.status_code)
    print("TEXT:", response.text)
    data = response.json()

    if response.status_code == 200:
      session['token'] = data['token']
      session['user'] = data['user']
      return redirect(url_for('dashboard.dashboard'))
    else:
      return redirect(url_for('landing.landing') + '?error=Error de conexión')

  except Exception:
    return redirect(url_for('landing.landing') + '?error=Error de conexión')
  
@login_bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('landing.landing'))