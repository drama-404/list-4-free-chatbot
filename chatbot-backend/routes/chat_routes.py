"""
Chat Routes Module

This module handles all chat-related routes for the List4Free chatbot.
It provides endpoints for initiating and completing chat sessions, managing
the conversation flow, and integrating with the main application.

Integration Points:
1. Frontend:
   - Receives search criteria from main app
   - Sends chat session data back to frontend
   - Handles WebSocket/SSE communication (TODO)

2. Database:
   - Manages chat sessions and user data
   - Handles transaction integrity
   - Provides error handling

3. Main Application:
   - Receives search criteria
   - Sends final preferences and user data
   - Manages user authentication state

Routes:
--------
POST /initiate
    - Initializes new chat session
    - Validates search criteria
    - Creates database record
    - Returns initial popup message

POST /complete
    - Completes chat session
    - Saves final preferences
    - Updates user contact info
    - Triggers main app integration
"""

from flask import Blueprint, request, jsonify
from database.db_utils import get_db
from models.models import ChatSession
from datetime import datetime
import uuid
from functools import wraps
import logging
import os

# Initialize Blueprint and logging
chat_bp = Blueprint('chat', __name__)
logger = logging.getLogger(__name__)

def handle_db_errors(f):
    """
    Decorator for handling database errors in route handlers.
    Provides consistent error logging and response format.
    
    Args:
        f: The route handler function to decorate
        
    Returns:
        Decorated function that handles database errors
    """
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
    """
    Initialize a new chat session with search criteria from the main app.
    
    Request Body:
        {
            "search_criteria": {
                "location": str,
                "propertyType": str,
                "bedrooms": {"min": int, "max": int},
                "price": {"min": int, "max": int}
            },
            "list4free_user_id": str (optional)
        }
    
    Returns:
        JSON response with session details and initial popup message
    """
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

        # # Generate initial popup message
        # initial_popup = generate_initial_popup(search_criteria, bool(data.get('list4free_user_id')))

        # Prepare frontend message
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        frontend_message = {
            'type': 'INITIATE_CHAT',
            'searchCriteria': search_criteria,
            'list4freeUserId': data.get('list4free_user_id')
        }
        
        # TODO: Implement WebSocket or Server-Sent Events for real-time communication
        return jsonify({
            'session_id': session_id,
            # 'initial_popup': initial_popup,
            'frontend_message': frontend_message
        }), 201

@chat_bp.route('/complete', methods=['POST'])
@handle_db_errors
def complete_chat():
    """
    Complete the chat session and send data to main app.
    
    Request Body:
        {
            "session_id": str,
            "final_preferences": dict,
            "user_email": str (optional),
            "conversation_summary": str (optional)
        }
    
    Returns:
        JSON response with completion status
    """
    try:
        data = request.get_json()
        logger.info(f"Received complete chat request with data: {data}")
        
        if not data or 'session_id' not in data or 'final_preferences' not in data:
            logger.error("Missing required fields in request")
            return jsonify({'error': 'Session ID and final preferences are required'}), 400
        
        # Log the incoming data
        logger.info(f"Session ID: {data['session_id']}")
        logger.info(f"Final preferences: {data['final_preferences']}")
        logger.info(f"User email: {data.get('user_email')}")
        
        with get_db() as db:
            session = db.query(ChatSession).filter(ChatSession.session_id == data['session_id']).first()
            
            if not session:
                logger.error(f"Session not found: {data['session_id']}")
                return jsonify({'error': 'Session not found'}), 404
            
            try:
                # Update session with final data
                session.final_preferences = data['final_preferences']
                session.user_email = data.get('user_email')
                session.conversation_summary = data.get('conversation_summary')
                session.closed_at = datetime.utcnow()
                session.is_active = False
                
                db.commit()
                logger.info(f"Successfully updated session {data['session_id']}")
                
                return jsonify({
                    'message': 'Chat session completed successfully',
                    'session_id': session.session_id
                }), 200
                
            except Exception as e:
                logger.error(f"Error updating session: {str(e)}")
                db.rollback()
                raise
                
    except Exception as e:
        logger.error(f"Error in complete_chat: {str(e)}")
        return jsonify({'error': str(e)}), 500

# def generate_initial_popup(search_criteria, is_logged_in=False):
#     """
#     Generate the initial popup message based on search criteria and user status.
    
#     Args:
#         search_criteria (dict): User's search criteria
#         is_logged_in (bool): Whether the user is logged into List4Free
        
#     Returns:
#         str: Formatted popup message
#     """
#     # TODO: Implement popup message generation
#     return ""
