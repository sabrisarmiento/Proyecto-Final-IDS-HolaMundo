from flask import Blueprint

marks_bp = Blueprint('marks', __name__)

@marks_bp.route("/notas", methods=["GET"])
def marks_list():
    try:
        