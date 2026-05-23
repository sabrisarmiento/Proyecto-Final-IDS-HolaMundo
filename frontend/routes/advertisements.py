from flask import Blueprint, render_template

advertisements_bp = Blueprint('advertisement', __name__)

@advertisements_bp.route('/avisos')
def advertisement():
  return render_template('advertisements.html', init="Advertisement is running")