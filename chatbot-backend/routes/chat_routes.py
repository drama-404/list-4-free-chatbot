from flask import Blueprint, request, jsonify
from database.db_utils import get_db
from models.models import ChatSession
from datetime import datetime
import uuid
from functools import wraps
import logging
import os

chat_bp = Blueprint('chat', __name__)
logger = logging.getLogger(__name__)

def handle_db_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    return decorated_function

@chat_bp.route('/initiate', methods=['POST'])
@handle_db_errors
def initiate_chat():
    """Initialize a new chat session with search criteria from the main app"""
    data = request.get_json()
    
    if not data or 'search_criteria' not in data:
        return jsonify({
            'error': 'Missing required field: search_criteria'
        }), 400

    # Validate search criteria structure
    search_criteria = data['search_criteria']
    required_fields = ['location', 'propertyType', 'bedrooms', 'price']
    for field in required_fields:
        if field not in search_criteria:
            return jsonify({
                'error': f'Missing required field in search_criteria: {field}'
            }), 400

    # Validate bedrooms and price structure
    if not isinstance(search_criteria['bedrooms'], dict) or 'min' not in search_criteria['bedrooms'] or 'max' not in search_criteria['bedrooms']:
        return jsonify({
            'error': 'bedrooms must be an object with min and max values'
        }), 400

    if not isinstance(search_criteria['price'], dict) or 'min' not in search_criteria['price'] or 'max' not in search_criteria['price']:
        return jsonify({
            'error': 'price must be an object with min and max values'
        }), 400

    with get_db() as db:
        # Create new chat session
        session_id = str(uuid.uuid4())
        chat_session = ChatSession(
            session_id=session_id,
            list4free_user_id=data.get('list4free_user_id'),
            initial_search_criteria=search_criteria,
            is_active=True
        )
        db.add(chat_session)
        db.flush()

        # Generate initial popup message
        initial_popup = generate_initial_popup(search_criteria, bool(data.get('list4free_user_id')))

        # Send message to frontend
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        frontend_message = {
            'type': 'INITIATE_CHAT',
            'searchCriteria': search_criteria,
            'list4freeUserId': data.get('list4free_user_id')
        }
        
        # TO DO use WebSocket or Server-Sent Events
        # For now, we'll just return the data the frontend wil handle it
        return jsonify({
            'session_id': session_id,
            'initial_popup': initial_popup,
            'frontend_message': frontend_message
        }), 201

@chat_bp.route('/complete', methods=['POST'])
@handle_db_errors
def complete_chat():
    """Complete the chat session and send data to main app"""
    data = request.get_json()
    if not data or 'session_id' not in data or 'final_preferences' not in data:
        return jsonify({'error': 'Session ID and final preferences are required'}), 400
    
    # Validate final preferences structure
    final_preferences = data['final_preferences']
    required_fields = ['location', 'propertyType', 'bedrooms', 'price']
    for field in required_fields:
        if field not in final_preferences:
            return jsonify({'error': f'Missing required field in final preferences: {field}'}), 400
    
    with get_db() as db:
        session = db.query(ChatSession).filter(ChatSession.session_id == data['session_id']).first()
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Update session with final data
        session.final_preferences = final_preferences
        session.user_email = data.get('user_email')
        session.conversation_summary = data.get('conversation_summary')
        session.closed_at = datetime.utcnow()
        session.is_active = False
        
        # TODO: Make API call to main app with the collected data
        # This should be done asynchronously to not block the response
        main_app_response = send_to_main_app({
            'session_id': session.session_id,
            'list4free_user_id': session.list4free_user_id,
            'user_email': session.user_email,
            'initial_search': session.initial_search_criteria,
            'final_preferences': session.final_preferences,
            'conversation_summary': session.conversation_summary
        })
        
        # Store the main app's search ID if provided
        if main_app_response and 'search_id' in main_app_response:
            session.main_app_search_id = main_app_response['search_id']
        
        return jsonify({
            'message': 'Chat session completed successfully',
            'main_app_search_id': session.main_app_search_id
        }), 200

def generate_initial_popup(search_criteria, is_logged_in=False):
    """Generate the initial popup message based on search criteria and user status"""
    return "Initial popup message"

def send_to_main_app(data):
    """Send collected data to main app"""
    # TODO: Implement API call to main app
    # This should be done asynchronously
    return {'search_id': 'placeholder-search-id'}
