# Main entry point for your Flask application.

from flask import Flask, request, jsonify
from flask_cors import CORS
from routes.chat_routes import chat_bp
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')  # Make sure  config.py is up and running
CORS(app)  # Enable CORS for all routes

# Register Blueprints
app.register_blueprint(chat_bp, url_prefix='/api/chat')

@app.route('/')
def index():
    return jsonify({'message': 'Chatbot API is up and running!'})

if __name__ == '__main__':
    app.run(debug=True)

