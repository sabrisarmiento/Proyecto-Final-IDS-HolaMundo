from flask import Blueprint, render_template
from services.material_frontend_service import MaterialFrontendService

materials_bp = Blueprint('materials', __name__)

@materials_bp.route('/materiales')
def public_materials():
    materiales_api = MaterialFrontendService.get_all()
    return render_template("materials.html", materiales=materiales_api)