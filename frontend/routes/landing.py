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
  return render_template('index.html', avisos=advertisements, clases=clases, active_page='landing')