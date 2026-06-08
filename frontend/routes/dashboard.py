from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
import requests

dashboard_bp = Blueprint('dashboard', __name__)

API = "http://127.0.0.1:5000"

@dashboard_bp.route('/dashboard')
def dashboard():
    token = session.get('token')
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debés iniciar sesión')

    headers = {'Authorization': f'Bearer {token}'}

    try:
        res = requests.get(f'{API}/dashboard/general', headers=headers)
        data = res.json() if res.ok else {}
    except Exception:
        data = {}

    return render_template(
        'dashboard.html',
        data=data,
        active_page='dashboard'
    )

@dashboard_bp.route('/dashboard/usuarios', methods=['POST'])
def crear_usuario():
    token = session.get('token')
    if not token:
        return jsonify({'ok': False, 'message': 'No autorizado'}), 401
    payload = request.get_json(silent=True) or {}
    try:
        res = requests.post(
            f'{API}/dashboard/usuarios',
            json=payload,
            headers={'Authorization': f'Bearer {token}'}
        )
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 502


@dashboard_bp.route('/dashboard/usuarios/<int:id_user>', methods=['PATCH'])
def actualizar_usuario(id_user):
    token = session.get('token')
    if not token:
        return jsonify({'ok': False, 'message': 'No autorizado'}), 401
    payload = request.get_json(silent=True) or {}
    try:
        res = requests.patch(
            f'{API}/dashboard/usuarios/{id_user}',
            json=payload,
            headers={'Authorization': f'Bearer {token}'}
        )
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 502


@dashboard_bp.route('/dashboard/usuarios/<int:id_user>', methods=['DELETE'])
def eliminar_usuario(id_user):
    token = session.get('token')
    if not token:
        return jsonify({'ok': False, 'message': 'No autorizado'}), 401
    try:
        res = requests.delete(
            f'{API}/dashboard/usuarios/{id_user}',
            headers={'Authorization': f'Bearer {token}'}
        )
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 502


@dashboard_bp.route('/dashboard/roles', methods=['POST'])
def crear_rol():
    token = session.get('token')
    if not token:
        return jsonify({'ok': False, 'message': 'No autorizado'}), 401
    payload = request.get_json(silent=True) or {}
    try:
        res = requests.post(
            f'{API}/dashboard/roles',
            json=payload,
            headers={'Authorization': f'Bearer {token}'}
        )
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 502


@dashboard_bp.route('/dashboard/roles/<int:id_rol>', methods=['DELETE'])
def eliminar_rol(id_rol):
    token = session.get('token')
    if not token:
        return jsonify({'ok': False, 'message': 'No autorizado'}), 401
    try:
        res = requests.delete(
            f'{API}/dashboard/roles/{id_rol}',
            headers={'Authorization': f'Bearer {token}'}
        )
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({'ok': False, 'message': str(e)}), 502