import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration settings (like database URI, secret key, etc.)

class Config:
    # Database configuration
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5433') 

    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    # API configuration
    API_PREFIX = '/api/v1'
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

    # Chat configuration
    MAX_SESSION_DURATION = int(os.getenv('MAX_SESSION_DURATION', '3600'))  # 1 hour in seconds
    MAX_MESSAGES_PER_SESSION = int(os.getenv('MAX_MESSAGES_PER_SESSION', '100'))

    @classmethod
    def get_database_url(cls):
        """Get the database URL for connection"""
        if not all([cls.DB_NAME, cls.DB_USER, cls.DB_PASSWORD]):
            raise ValueError("Missing required database configuration. Please check your .env file.")
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

