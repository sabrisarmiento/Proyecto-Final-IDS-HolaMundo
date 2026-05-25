from flask import Blueprint, render_template
import requests 

advertisements_bp = Blueprint('advertisements', __name__)

@advertisements_bp.route('/avisos', methods=['GET'])
def public_advertisements():
    try:
        response = requests.get('http://localhost:5000/advertisements')
        data = response.json()
        
        if data.get('ok'):
            advertisements = data.get('data') 
        else:
            advertisements = []
            
    except Exception as e:
        advertisements = []

    return render_template('advertisements.html', advertisements=advertisements)