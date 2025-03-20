# Configuration settings (like database URI, secret key, etc.)

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/chatbot'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key_here'
    REACT_APP_API_URL = 'http://localhost:5000'
    REACT_APP_CHAT_API_URL = '/api/chat/start'

