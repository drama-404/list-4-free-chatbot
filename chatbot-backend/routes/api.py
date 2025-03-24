from flask import Blueprint, request, jsonify
from models.chat_session import ChatSession
from models.search_filter import SearchFilter
from models.user_contact import UserContact
from models.scraping_task import ScrapingTask
from services.database import db

api = Blueprint('api', __name__)

@api.route('/search', methods=['POST'])
def create_search():
    try:
        data = request.json
        
        # Create new chat session
        session = ChatSession(
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(session)
        
        # Create search filters
        search_filter = SearchFilter(
            session_id=session.session_id,
            location=data.get('location'),
            property_type=data.get('property_type'),
            bedrooms_min=data.get('bedrooms_min'),
            bedrooms_max=data.get('bedrooms_max'),
            needs_public_transport=data.get('needs_public_transport'),
            needs_schools=data.get('needs_schools'),
            timeline=data.get('timeline'),
            has_loan_approval=data.get('has_loan_approval')
        )
        db.session.add(search_filter)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'session_id': session.session_id,
            'search_id': search_filter.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api.route('/contact', methods=['POST'])
def save_contact():
    try:
        data = request.json
        session_id = data.get('session_id')
        
        contact = UserContact(
            session_id=session_id,
            email=data.get('email')
        )
        db.session.add(contact)
        
        # Create scraping task
        search_filter = SearchFilter.query.filter_by(session_id=session_id).first()
        if search_filter:
            task = ScrapingTask(search_filter_id=search_filter.id)
            db.session.add(task)
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Contact information saved and scraping task created'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500