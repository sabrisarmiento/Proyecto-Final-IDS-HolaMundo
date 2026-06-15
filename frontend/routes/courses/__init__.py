from flask import Blueprint

courses_bp = Blueprint('courses', __name__)

from . import general, detail, teams, marks, classes, config