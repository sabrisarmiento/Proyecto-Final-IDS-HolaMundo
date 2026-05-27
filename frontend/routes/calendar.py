from flask import Blueprint, render_template
import requests

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/cronograma', methods=['GET'])
def calendar():
  schedule = [
    {
      "week": 11,
      "classes": [
        {
          "type": "Teórica",
          "date": "19/05",
          "topics": ["Archivos de texto", "CSV"],
          "modality": "Virtual"
        },
        {
          "type": "Práctica",
          "date": "21/05",
          "topics": ["Archivos CSV"],
          "modality": "Presencial"
        }
      ]
    },
    {
      "week": 12,
      "classes": [
        {
          "type": "Teórica",
          "date": "26/05",
          "topics": ["Bases de Datos", "SQL (Introducción)"],
          "modality": "Virtual"
        },
        {
          "type": "Práctica",
          "date": "28/05",
          "topics": ["Consultas SQL básicas"],
          "modality": "Virtual"
        }
      ]
    }
  ]
  
  return render_template('calendar.html', schedule=schedule, active_page='calendar')