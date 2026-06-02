from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__)
"""
@dashboard_bp.route('/dashboard')
def dashboard():
    stats = {
    "total_alumnos": 120,
    "equipos": 15,
    "asistencia_promedio": "84%",
    "aprobados": 92,
    "desaprobados": 28,
    "promedio_general": 7.8,
    }
    alumnos = [
    {
        "nombre": "Juan",
        "apellido": "Pérez",
        "padron": "109283",
        "parcial1": 8,
        "parcial2": 7,
        "tp": 9,
        "equipo": "Equipo 1",
        "asistencia": "92%",
        "activo": True
    },
    {
        "nombre": "Ana",
        "apellido": "Gómez",
        "padron": "109284",
        "parcial1": 3,
        "parcial2": 4,
        "tp": 6,
        "equipo": "Equipo 2",
        "asistencia": "65%",
        "activo": False
    },
    {
        "nombre": "Lucas",
        "apellido": "Martinez",
        "padron": "109285",
        "parcial1": 9,
        "parcial2": 8,
        "tp": 10,
        "equipo": "Equipo 1",
        "asistencia": "96%",
        "activo": True
    }
    ]
    equipos = [
        {
            "nombre": "Equipo 1",
            "integrantes": "Juan, Lorenzo, Carlos"
        },
        {
            "nombre": "Equipo 2",
            "integrantes": "Lucas, Pedro, Vilma"
        }
    ]
    return render_template("dashboard.html", stats=stats, alumnos=alumnos, equipos=equipos, active_page="dashboard")
"""

@dashboard_bp.route('/dashboard')
def dashboard():
    stats = {
    "total_alumnos": 120,
    "equipos": 15,
    "asistencia_promedio": "84%",
    "aprobados": 92,
    "desaprobados": 28,
    "promedio_general": 7.8,
    }
    alumnos = [
    {
        "nombre": "Juan",
        "apellido": "Pérez",
        "padron": "109283",
        "parcial1": 8,
        "parcial2": 7,
        "tp": 9,
        "equipo": "Equipo 1",
        "asistencia": "92%",
        "activo": True
    },
    {
        "nombre": "Ana",
        "apellido": "Gómez",
        "padron": "109284",
        "parcial1": 3,
        "parcial2": 4,
        "tp": 6,
        "equipo": "Equipo 2",
        "asistencia": "65%",
        "activo": False
    },
    {
        "nombre": "Lucas",
        "apellido": "Martinez",
        "padron": "109285",
        "parcial1": 9,
        "parcial2": 8,
        "tp": 10,
        "equipo": "Equipo 1",
        "asistencia": "96%",
        "activo": True
    }
    ]
    equipos = [
        {
            "nombre": "Equipo 1",
            "integrantes": "Juan, Lorenzo, Carlos"
        },
        {
            "nombre": "Equipo 2",
            "integrantes": "Lucas, Pedro, Vilma"
        }
    ]
    Profesor = [
        {"nombre": "Bruno",
        "apellido": "Lanzillota",
        "correo": "bruno@fiuba.com"}
    ]
    
    Ayudantes = [
        {"nombre": "Leonel",
        "apellido": "chaves",
        "correo": "leonel@fiuba.com"},
        {"nombre": "Tomás",
        "apellido": "Rodríguez",
        "correo": "tomas@fiuba.com"},
        {"nombre": "Nestor",
        "apellido": "Palavecino",
        "correo": "nestor@fiuba.com"}
    ]
    return render_template("dashboard.html", Profesor=Profesor, Ayudantes=Ayudantes, stats=stats, alumnos=alumnos, equipos=equipos, active_page="dashboard")