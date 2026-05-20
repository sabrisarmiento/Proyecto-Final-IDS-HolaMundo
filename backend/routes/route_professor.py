from flask import Blueprint
from handlers.professor_handler import professors_handler

professor_bp = Blueprint('professor', __name__)

@professor_bp.route('/professor', methods=['GET'])
def professor():
  return professors_handler()