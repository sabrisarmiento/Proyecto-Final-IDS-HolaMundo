from flask import Blueprint, render_template
from services.advertisement_frontend_service import AdvertisementFrontendService
import requests 

advertisements_bp = Blueprint('advertisements', __name__)

@advertisements_bp.route('/avisos')
def public_advertisements():
    avisos = AdvertisementFrontendService.get_all()
    return render_template("advertisements.html", avisos=avisos)