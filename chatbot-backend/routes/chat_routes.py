from flask import Blueprint, request, jsonify
from database.db_utils import get_db
from models.models import ChatSession, ChatMessage, PropertyPreference, SearchHistory, ConversationState
from datetime import datetime
import uuid

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/session', methods=['POST'])
def create_session():
    """Create a new chat session"""
    with get_db() as db:
        session = ChatSession()
        db.add(session)
        db.flush()  # Get the session ID without committing
        
        # Initialize conversation state
        state = ConversationState(
            session_id=session.id,
            current_step='initial_popup'
        )
        db.add(state)
        
        return jsonify({
            'session_id': session.session_id,
            'created_at': session.created_at.isoformat()
        }), 201

@chat_bp.route('/session/<session_id>/message', methods=['POST'])
def send_message(session_id):
    """Send a message in a chat session"""
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'error': 'Message content is required'}), 400
    
    with get_db() as db:
        session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Save user message
        user_message = ChatMessage(
            session_id=session.id,
            message_type='user',
            content=data['content']
        )
        db.add(user_message)
        
        # Update session last active
        session.last_active = datetime.utcnow()
        
        # TODO: Process message with chatbot logic and generate response
        # For now, return a placeholder response
        bot_message = ChatMessage(
            session_id=session.id,
            message_type='bot',
            content='Thank you for your message. This is a placeholder response.'
        )
        db.add(bot_message)
        
        return jsonify({
            'user_message': {
                'content': user_message.content,
                'timestamp': user_message.created_at.isoformat()
            },
            'bot_message': {
                'content': bot_message.content,
                'timestamp': bot_message.created_at.isoformat()
            }
        }), 200

@chat_bp.route('/session/<session_id>/preferences', methods=['POST'])
def update_preferences(session_id):
    """Update property preferences for a session"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Preferences data is required'}), 400
    
    with get_db() as db:
        session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Update or create preferences
        preferences = db.query(PropertyPreference).filter(
            PropertyPreference.session_id == session.id
        ).first()
        
        if not preferences:
            preferences = PropertyPreference(session_id=session.id)
            db.add(preferences)
        
        # Update preferences with new data
        for key, value in data.items():
            if hasattr(preferences, key):
                setattr(preferences, key, value)
        
        return jsonify({
            'message': 'Preferences updated successfully',
            'preferences': {
                'location': preferences.location,
                'property_type': preferences.property_type,
                'property_subtype': preferences.property_subtype,
                'min_bedrooms': preferences.min_bedrooms,
                'max_bedrooms': preferences.max_bedrooms,
                'min_price': float(preferences.min_price) if preferences.min_price else None,
                'max_price': float(preferences.max_price) if preferences.max_price else None,
                'has_transport': preferences.has_transport,
                'has_school': preferences.has_school,
                'timeline': preferences.timeline,
                'has_pre_approved_loan': preferences.has_pre_approved_loan
            }
        }), 200

@chat_bp.route('/session/<session_id>/search', methods=['POST'])
def save_search(session_id):
    """Save a search query to history"""
    data = request.get_json()
    if not data or 'search_criteria' not in data:
        return jsonify({'error': 'Search criteria is required'}), 400
    
    with get_db() as db:
        session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        search = SearchHistory(
            session_id=session.id,
            search_criteria=data['search_criteria'],
            is_deep_search=data.get('is_deep_search', False)
        )
        db.add(search)
        
        return jsonify({
            'message': 'Search saved successfully',
            'search_id': search.id,
            'created_at': search.created_at.isoformat()
        }), 201

@chat_bp.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get session details including messages and preferences"""
    with get_db() as db:
        session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Get related data
        messages = db.query(ChatMessage).filter(ChatMessage.session_id == session.id).all()
        preferences = db.query(PropertyPreference).filter(
            PropertyPreference.session_id == session.id
        ).first()
        state = db.query(ConversationState).filter(
            ConversationState.session_id == session.id
        ).first()
        
        return jsonify({
            'session_id': session.session_id,
            'created_at': session.created_at.isoformat(),
            'last_active': session.last_active.isoformat(),
            'is_active': session.is_active,
            'messages': [{
                'type': msg.message_type,
                'content': msg.content,
                'timestamp': msg.created_at.isoformat()
            } for msg in messages],
            'preferences': {
                'location': preferences.location if preferences else None,
                'property_type': preferences.property_type if preferences else None,
                'property_subtype': preferences.property_subtype if preferences else None,
                'min_bedrooms': preferences.min_bedrooms if preferences else None,
                'max_bedrooms': preferences.max_bedrooms if preferences else None,
                'min_price': float(preferences.min_price) if preferences and preferences.min_price else None,
                'max_price': float(preferences.max_price) if preferences and preferences.max_price else None,
                'has_transport': preferences.has_transport if preferences else False,
                'has_school': preferences.has_school if preferences else False,
                'timeline': preferences.timeline if preferences else None,
                'has_pre_approved_loan': preferences.has_pre_approved_loan if preferences else None
            },
            'current_step': state.current_step if state else None
        }), 200
