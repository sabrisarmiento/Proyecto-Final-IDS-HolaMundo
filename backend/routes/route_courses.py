from flask import Blueprint
from services.courses_service import (
  courses_service
)

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/courses', methods=['GET'])
def get_courses():
  return courses_service()