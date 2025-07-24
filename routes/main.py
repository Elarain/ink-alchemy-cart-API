from flask import Blueprint, jsonify, g, current_app
from datetime import datetime
import time

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Middleware API is running',
        'timestamp': datetime.utcnow().isoformat(),
        'request_id': g.request_id
    })

@main_bp.route('/health')
def health():
    """Health check endpoint"""
    start_time = current_app.config.get('START_TIME', time.time())
    return jsonify({
        'status': 'healthy',
        'uptime': time.time() - start_time,
        'timestamp': datetime.utcnow().isoformat(),
        'request_id': g.request_id
    })