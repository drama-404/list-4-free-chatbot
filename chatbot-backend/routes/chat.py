"""
Chat Routes Module

This module handles all chat-related routes and integrates with the property
scraping functionality to provide property search results.
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any, Optional
import logging
from ..models import ChatSession
from ..database import get_db
from ..scrapers import ScraperController, RightmoveScraper

logger = logging.getLogger(__name__)
chat_bp = Blueprint('chat', __name__)

# Initialize scraper controller
scraper_controller = None

async def initialize_scrapers():
    """Initialize the scraper controller with available scrapers."""
    global scraper_controller
    if not scraper_controller:
        scrapers = [
            RightmoveScraper()
        ]
        scraper_controller = ScraperController(scrapers)
        await scraper_controller.initialize()

@chat_bp.route('/initiate', methods=['POST'])
async def initiate_chat():
    """Initialize a new chat session."""
    try:
        data = request.get_json()
        search_criteria = data.get('search_criteria', {})
        list4free_user_id = data.get('list4free_user_id')

        # Create new chat session
        with get_db() as db:
            session = ChatSession(
                list4free_user_id=list4free_user_id,
                initial_search_criteria=search_criteria,
                is_active=True
            )
            db.add(session)
            db.commit()
            db.refresh(session)

        return jsonify({
            'session_id': str(session.session_id),
            'initial_popup': "Hello! I'm your property search assistant. I'll help you find your perfect home.",
            'frontend_message': {
                'type': 'INITIATE_CHAT',
                'searchCriteria': search_criteria,
                'list4freeUserId': list4free_user_id
            }
        })

    except Exception as e:
        logger.error(f"Failed to initiate chat: {str(e)}")
        return jsonify({'error': 'Failed to initiate chat'}), 500

@chat_bp.route('/complete', methods=['POST'])
async def complete_chat():
    """Complete a chat session and perform property search."""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        final_preferences = data.get('final_preferences', {})
        user_email = data.get('user_email')
        conversation_summary = data.get('conversation_summary', [])

        # Update chat session
        with get_db() as db:
            session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
            if not session:
                return jsonify({'error': 'Chat session not found'}), 404

            session.final_preferences = final_preferences
            session.user_email = user_email
            session.conversation_summary = conversation_summary
            session.is_active = False
            db.commit()

        # Initialize scrapers if not already done
        await initialize_scrapers()

        # Perform property search
        search_criteria = {
            'location': final_preferences.get('location'),
            'price_min': final_preferences.get('price', {}).get('min'),
            'price_max': final_preferences.get('price', {}).get('max'),
            'bedrooms_min': final_preferences.get('bedrooms', {}).get('min'),
            'bedrooms_max': final_preferences.get('bedrooms', {}).get('max'),
            'property_type': final_preferences.get('propertyType')
        }

        # Get property listings
        listings = await scraper_controller.search(search_criteria, max_results=10)

        # Clean up scrapers
        await scraper_controller.cleanup()

        return jsonify({
            'message': 'Chat session completed successfully',
            'session_id': session_id,
            'property_listings': [listing.to_dict() for listing in listings]
        })

    except Exception as e:
        logger.error(f"Failed to complete chat: {str(e)}")
        return jsonify({'error': 'Failed to complete chat'}), 500 