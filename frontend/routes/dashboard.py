import os
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import requests
from helpers.logger import log_action
from config import get_user

dashboard_bp = Blueprint('dashboard', __name__)

API = os.getenv("BACKEND_URL", "http://127.0.0.1:5000")


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
    user = session.get('user', {})
    token = session.get('token')
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debés iniciar sesión')

    payload = {
        'nombre':     request.form.get('nombre'),
        'apellido':   request.form.get('apellido'),
        'correo':     request.form.get('correo'),
        'contraseña': request.form.get('contraseña'),
        'id_rol':     int(request.form.get('id_rol', 1)),
    }

    try:
        res = requests.post(
            f'{API}/dashboard/usuarios',
            json=payload,
            headers={'Authorization': f'Bearer {token}'}
        )
        if res.status_code in (200, 201):
            flash('Usuario creado correctamente', 'ok')
        else:
            body = res.json() if res.content else {}
            desc = (body.get('errors') or [{}])[0].get('description', 'No se pudo crear el usuario')
            flash(desc, 'error')
        log_action(
            method='POST',
            description=f'Creó al usuario {payload["nombre"]} {payload["apellido"]} con el rol {payload["id_rol"]}',
            user_id=user.get('id_usuario', 'desconocido'),
            user_email=user.get('correo', 'desconocido'),
            status_code=res.status_code
        )
    except Exception as e:
        flash(f'Error de conexión: {e}', 'error')

    return redirect(url_for('dashboard.dashboard'))


@dashboard_bp.route('/dashboard/usuarios/<int:id_user>', methods=['POST'])
def actualizar_usuario(id_user):
    user = get_user()
    token = session.get('token')
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debés iniciar sesión')

    payload = {
        'nombre':   request.form.get('nombre'),
        'apellido': request.form.get('apellido'),
        'correo':   request.form.get('correo'),
        'id_rol':   int(request.form.get('id_rol', 1)),
    }

    try:
        res = requests.patch(
            f'{API}/dashboard/usuarios/{id_user}',
            json=payload,
            headers={'Authorization': f'Bearer {token}'}
        )
        log_action(
            method='PATCH',
            description=f'Se actualizo el usuario de {payload["nombre"]} y correo {payload["correo"]}',
            user_id=user.get('id_usuario', 'desconocido'),
            user_email=user.get('correo', 'desconocido'),
            status_code=res.status_code
        )
        if res.status_code == 200:
            flash('Usuario actualizado correctamente', 'ok')
        else:
            body = res.json() if res.content else {}
            desc = (body.get('errors') or [{}])[0].get('description', 'No se pudo actualizar el usuario')
            flash(desc, 'error')
    except Exception as e:
        flash(f'Error de conexión: {e}', 'error')

    return redirect(url_for('dashboard.dashboard'))


@dashboard_bp.route('/dashboard/usuarios/<int:id_user>/eliminar', methods=['POST'])
def eliminar_usuario(id_user):
    user = get_user()
    token = session.get('token')
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debés iniciar sesión')

    try:
        res = requests.delete(
            f'{API}/dashboard/usuarios/{id_user}',
            headers={'Authorization': f'Bearer {token}'}
        )
        log_action(
            method='PATCH',
            description=f'Se elimino al usuario {id_user}',
            user_id=user.get('id_usuario', 'desconocido'),
            user_email=user.get('correo', 'desconocido'),
            status_code=res.status_code
        )
        if res.status_code == 200:
            flash('Usuario eliminado correctamente', 'ok')
        else:
            flash('No se pudo eliminar el usuario', 'error')
    except Exception as e:
        flash(f'Error de conexión: {e}', 'error')

    return redirect(url_for('dashboard.dashboard'))


@dashboard_bp.route('/dashboard/roles', methods=['POST'])
def crear_rol():
    user = get_user()
    token = session.get('token')
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debés iniciar sesión')

    payload = {
        'nombre':               request.form.get('nombre'),
        'nivel_administracion': int(request.form.get('nivel_administracion', 1)),
    }

    try:
        res = requests.post(
            f'{API}/dashboard/roles',
            json=payload,
            headers={'Authorization': f'Bearer {token}'}
        )
        log_action(
            method='PATCH',
            description=f'Se creo el rol {payload["nombre"]}',
            user_id=user.get('id_usuario', 'desconocido'),
            user_email=user.get('correo', 'desconocido'),
            status_code=res.status_code
        )
        if res.status_code in (200, 201):
            flash('Rol creado correctamente', 'ok')
        else:
            body = res.json() if res.content else {}
            desc = (body.get('errors') or [{}])[0].get('description', 'No se pudo crear el rol')
            flash(desc, 'error')
    except Exception as e:
        flash(f'Error de conexión: {e}', 'error')

    return redirect(url_for('dashboard.dashboard'))


@dashboard_bp.route('/dashboard/roles/<int:id_rol>/eliminar', methods=['POST'])
def eliminar_rol(id_rol):
    user = get_user()
    token = session.get('token')
    if not token:
        return redirect(url_for('landing.landing') + '?error=Debés iniciar sesión')

    try:
        res = requests.delete(
            f'{API}/dashboard/roles/{id_rol}',
            headers={'Authorization': f'Bearer {token}'}
        )
        log_action(
            method='PATCH',
            description=f'Se elimino el rol {id_rol}',
            user_id=user.get('id_usuario', 'desconocido'),
            user_email=user.get('correo', 'desconocido'),
            status_code=res.status_code
        )
        if res.status_code in (200, 204):
            flash('Rol eliminado correctamente', 'ok')
        else:
            flash('No se pudo eliminar el rol', 'error')
    except Exception as e:
        flash(f'Error de conexión: {e}', 'error')

    return redirect(url_for('dashboard.dashboard'))