from flask import Blueprint, render_template

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/')
def landing():
  avisos = [
    {
      'titulo': 'Aviso 1',
      "id_aviso": 1,
    },
    {
      'titulo': 'Aviso 2',
      "id_aviso": 2,
    },
    {
      'titulo': 'Aviso 3',
      "id_aviso": 3,
    }
  ]

  clases = [
    {
      'nombre': 'Clase 1',
      "id_clase": 1,
      "tipo": "Teórica",
      "tema": "Introducción a la programación"
    },
    {
      'nombre': 'Clase 2',
      "id_clase": 2,
      "tipo": "Práctica",
      "tema": "Ejercicios de programación"
    },
    {
      'nombre': 'Clase 3',
      "id_clase": 3,
      "tipo": "Teórica",
      "tema": "Estructuras de datos"
    },
    {
      'nombre': 'Clase 4',
      "id_clase": 4,
      "tipo": "Práctica",
      "tema": "Estructuras de datos"
    },
    {
      'nombre': 'Clase 5',
      "id_clase": 5,
      "tipo": "Teórica",
      "tema": "Algoritmos"
    },
    {
      'nombre': 'Clase 6',
      "id_clase": 6,
      "tipo": "Práctica",
      "tema": "Algoritmos"
    }
  ]
  return render_template('index.html', avisos=avisos, clases=clases)