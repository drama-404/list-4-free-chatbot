"""
List4Free Chatbot Backend

Main entry point for the Flask application that powers the List4Free chatbot.
Handles server configuration, CORS, and route registration.

Features:
---------
1. CORS Configuration
   - Allows requests from frontend (localhost:3000)
   - Supports necessary HTTP methods and headers

2. Route Registration
   - Chat routes for session management
   - API versioning (v1)

3. Database Integration
   - Automatic database initialization
   - Connection management

4. Environment Management
   - Loads configuration from .env
   - Supports development and production settings

Usage:
------
1. Development:
   python app.py

2. Production:
   gunicorn app:app
"""

from flask import Flask
from flask_cors import CORS
from config import Config
from routes.chat_routes import chat_bp
from database.db_utils import init_db
import os
from dotenv import load_dotenv

def load_environment():
    """
    Load and validate environment variables.
    Logs important configuration details for debugging.
    """
    print("Current working directory:", os.getcwd())
    print("Looking for .env file...")
    load_dotenv()
    
    # Log database configuration (mask sensitive data)
    db_config = {
        'DB_NAME': os.getenv('DB_NAME'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_PORT': os.getenv('DB_PORT')
    }
    print("Environment variables loaded:", db_config)

def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize CORS with development settings
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Accept"]
        }
    })
    
    # Register blueprints with API versioning
    app.register_blueprint(chat_bp, url_prefix=f"{Config.API_PREFIX}/chat")
    
    # Initialize database connection
    init_db()
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Load environment variables
    load_environment()
    
    # Start the development server
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5000,       # Default Flask port
        debug=Config.DEBUG
    )

