from flask import Flask
from flask_cors import CORS
import time
import logging
import sys

# Import blueprints
from routes.main import main_bp
from routes.replicate import replicate_bp

# Import middleware
from middleware import register_middleware

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('api.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Register middleware
    register_middleware(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(replicate_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    start_time = time.time()
    
    print(f"Starting Middleware API server...")
    print(f"Server will run on http://localhost:5000")
    print(f"Available routes:")
    print(f"  GET  /                 - Basic info")
    print(f"  GET  /health           - Health check")
    print(f"  GET  /api/replicate        - replicate endpoint")
    
    # Store start time for health check
    app.config['START_TIME'] = start_time
    
    app.run(host='0.0.0.0', port=5000, debug=True)