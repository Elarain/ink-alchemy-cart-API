from flask import g, request, jsonify
import time
import uuid
from datetime import datetime

def register_middleware(app):
    """Register all middleware with the Flask app"""
    
    @app.before_request
    def before_request():
        """Middleware that runs before each request"""
        g.start_time = time.time()
        g.request_id = str(uuid.uuid4())[:8]
        
        # Log request details
        app.logger.info(f"Request {g.request_id}: {request.method} {request.path}")

    @app.after_request
    def after_request(response):
        """Middleware that runs after each request"""
        # Add request ID to response headers
        response.headers['X-Request-ID'] = getattr(g, 'request_id', 'unknown')
        
        # Calculate and add response time
        if hasattr(g, 'start_time'):
            duration = (time.time() - g.start_time) * 1000
            response.headers['X-Response-Time'] = f"{duration:.2f}ms"
            
            # Log response details
            app.logger.info(f"Request {g.request_id} completed in {duration:.2f}ms with status {response.status_code}")
        
        return response

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 errors"""
        return jsonify({
            'error': 'Bad Request',
            'message': str(error.description),
            'request_id': getattr(g, 'request_id', 'unknown'),
            'timestamp': datetime.utcnow().isoformat()
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'error': 'Route not found',
            'path': request.path,
            'method': request.method,
            'request_id': getattr(g, 'request_id', 'unknown'),
            'timestamp': datetime.utcnow().isoformat()
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        app.logger.error(f"Internal error in request {getattr(g, 'request_id', 'unknown')}: {str(error)}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Something went wrong!',
            'request_id': getattr(g, 'request_id', 'unknown'),
            'timestamp': datetime.utcnow().isoformat()
        }), 500