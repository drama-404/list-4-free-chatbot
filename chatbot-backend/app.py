# Main entry point for your Flask application.

from flask import Flask
from flask_cors import CORS
from config import Config
from routes.chat_routes import chat_bp
from database.db_utils import init_db
import os
from dotenv import load_dotenv

# Load environment variables
print("Current working directory:", os.getcwd())
print("Looking for .env file...")
load_dotenv()
print("Environment variables loaded:", {
    'DB_NAME': os.getenv('DB_NAME'),
    'DB_USER': os.getenv('DB_USER'),
    'DB_HOST': os.getenv('DB_HOST'),
    'DB_PORT': os.getenv('DB_PORT')
})

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize CORS with more permissive settings for development
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Accept"]
        }
    })
    
    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix=f"{Config.API_PREFIX}/chat")
    
    # Initialize database
    init_db()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)

