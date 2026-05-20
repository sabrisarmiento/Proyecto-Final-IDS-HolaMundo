from flask import Blueprint, jsonify
from handlers.assistant_handler import assistants_handler, assistant_handler

assistant_bp = Blueprint('assistant', __name__)

@assistant_bp.route('/assistant', methods=['GET'])
def assistant():
  return assistants_handler()
  
@assistant_bp.route('/assistant/<int:id>', methods=['GET'])
def assistant_by_id(id):
  return assistant_handler(id)