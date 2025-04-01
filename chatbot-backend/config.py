"""
Configuration Module

This module manages all configuration settings for the List4Free chatbot.
It loads environment variables from .env and provides default values where appropriate.

Configuration Categories:
------------------------
1. Database Settings
   - Connection details for Azure PostgreSQL
   - Connection pooling and timeout settings

2. Flask Settings
   - Secret key for session management
   - Debug mode configuration

3. API Settings
   - Version prefix for all endpoints
   - CORS configuration for frontend access

4. Chat Settings
   - Session duration limits
   - Message count limits

Environment Variables:
--------------------
Required:
- DB_NAME: Database name
- DB_USER: Database username
- DB_PASSWORD: Database password
- SECRET_KEY: Flask secret key

Optional:
- DB_HOST: Database host (default: localhost)
- DB_PORT: Database port (default: 5433)
- FLASK_DEBUG: Enable debug mode (default: False)
- CORS_ORIGINS: Allowed origins (default: http://localhost:3000)
- MAX_SESSION_DURATION: Session timeout in seconds (default: 3600)
- MAX_MESSAGES_PER_SESSION: Message limit per session (default: 100)
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class that centralizes all application settings.
    Loads values from environment variables with sensible defaults.
    """
    
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
        """
        Construct the database URL for SQLAlchemy connection.
        
        Returns:
            str: PostgreSQL connection URL
            
        Raises:
            ValueError: If required database configuration is missing
        """
        if not all([cls.DB_NAME, cls.DB_USER, cls.DB_PASSWORD]):
            raise ValueError("Missing required database configuration. Please check your .env file.")
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

    @classmethod
    def validate_config(cls):
        """
        Validate all configuration settings.
        
        Returns:
            bool: True if configuration is valid
            
        Raises:
            ValueError: If any required settings are missing or invalid
        """
        # Check required environment variables
        required_vars = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'SECRET_KEY']
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True

