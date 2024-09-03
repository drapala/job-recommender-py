from flask import Blueprint, jsonify, request, current_app
from .services import generate_recommendations
from .models import db, Job

bp = Blueprint('main', __name__)

@bp.route('/generate_recommendations', methods=['POST'])
def generate_recommendations_route():
    try:
        recommendations = generate_recommendations()
        return jsonify({'status': 'success', 'data': recommendations})
    except Exception as e:
        current_app.logger.error(f"Error generating recommendations: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200
