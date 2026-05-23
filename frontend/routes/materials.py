from flask import Blueprint, render_template

materials_bp = Blueprint('materials', __name__)

@materials_bp.route('/materiales')
def materials():
  return render_template('materials.html', init="Materials is running")