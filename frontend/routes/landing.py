from flask import Blueprint, render_template
import requests

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/', methods=["GET"])
def landing():
  try:
    response = requests.get('http://127.0.0.1:5000/advertisements')
    data = response.json()
    advertisements = data.get("advertisements") or data.get("data") or []
    advertisements = advertisements[-3:][::-1]

  except Exception as e:
    advertisements = []

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
  return render_template('index.html', avisos=advertisements, clases=clases)