"""
Chat Routes Module with Property Scraping Integration

This module extends the basic chat functionality to include property scraping.
It should be used when implementing the property scraping feature.

IMPORTANT: This file is currently NOT in use. To integrate property scraping:
1. Replace the contents of chat_routes.py with this file
2. Update the imports in __init__.py to use this module
3. Ensure the database schema includes the scraped_properties table
4. Test the scraping functionality before deploying

The main differences from chat_routes.py are:
- Async/await support for scraping operations
- Property scraping and saving functionality
- Extended response format to include property listings

See the README.md for more details on the scraping implementation.
"""

from flask import Blueprint, request, jsonify
from database.db_utils import get_db
from models.models import ChatSession, ScrapedProperty
from datetime import datetime
import uuid
from functools import wraps
import logging
import os
import json
import asyncio
from scrapers import ScraperController, RightmoveScraper

# Initialize Blueprint and logging
chat_bp = Blueprint('chat', __name__)
logger = logging.getLogger(__name__)

# Initialize scraper controller
scraper_controller = None

async def initialize_scrapers():
    """
    Initialize the scraper controller with available scrapers.
    This function should be called before performing any scraping operations.
    """
    global scraper_controller
    if not scraper_controller:
        scrapers = [RightmoveScraper()]
        scraper_controller = ScraperController(scrapers)
        await scraper_controller.initialize()

def save_scraped_properties(db, session_id, listings):
    """
    Save scraped property listings to the database.
    Handles null/optional fields safely.
    
    Args:
        db: Database session
        session_id: ID of the chat session
        listings: List of property listings to save
    """
    try:
        for listing in listings:
            property_data = listing.to_dict()
            
            # Safely extract nested data with defaults
            location = property_data.get('location', {})
            features = property_data.get('features', {})
            price = property_data.get('price', {})
            media = property_data.get('media', {})
            availability = property_data.get('availability', {})
            agent = property_data.get('agent', {})
            
            scraped_property = ScrapedProperty(
                session_id=session_id,
                listing_id=property_data.get('listing_id'),
                source=property_data.get('source'),
                url=property_data.get('url'),
                title=property_data.get('title'),
                description=property_data.get('description'),
                # Location data
                address=location.get('address'),
                city=location.get('city'),
                postcode=location.get('postcode'),
                region=location.get('region'),
                country=location.get('country'),
                latitude=location.get('latitude'),
                longitude=location.get('longitude'),
                # Features
                bedrooms=features.get('bedrooms'),
                bathrooms=features.get('bathrooms'),
                reception_rooms=features.get('reception_rooms'),
                property_type=features.get('property_type'),
                tenure=features.get('tenure'),
                floor_area=features.get('floor_area'),
                year_built=features.get('year_built'),
                features=features.get('features'),
                energy_rating=features.get('energy_rating'),
                council_tax_band=features.get('council_tax_band'),
                # Price information
                price_amount=price.get('amount'),
                price_currency=price.get('currency'),
                price_type=price.get('price_type'),
                is_under_offer=price.get('is_under_offer'),
                is_sold=price.get('is_sold'),
                sold_date=price.get('sold_date'),
                sold_price=price.get('sold_price'),
                # Media
                images=media.get('images'),
                floor_plans=media.get('floor_plans'),
                virtual_tour_url=media.get('virtual_tour_url'),
                # Availability
                available_from=availability.get('available_from'),
                last_updated=availability.get('last_updated'),
                # Agent information
                agent_name=agent.get('name'),
                agent_company=agent.get('company'),
                agent_phone=agent.get('phone'),
                agent_email=agent.get('email'),
                agent_website=agent.get('website'),
                # Raw data
                raw_data=property_data.get('raw_data')
            )
            db.add(scraped_property)
        db.commit()
        logger.info(f"Successfully saved {len(listings)} properties for session {session_id}")
    except Exception as e:
        logger.error(f"Error saving scraped properties: {str(e)}")
        db.rollback()
        raise

async def perform_scraping(session_id, search_criteria):
    """
    Perform property scraping asynchronously.
    
    Args:
        session_id: ID of the chat session
        search_criteria: Dictionary containing search parameters
        
    Returns:
        List of property listings
    """
    try:
        # Initialize scrapers
        await initialize_scrapers()
        
        # Get property listings
        listings = await scraper_controller.search(search_criteria, max_results=5)
        
        # Save to database
        with get_db() as db:
            save_scraped_properties(db, session_id, listings)
        
        # Clean up
        await scraper_controller.cleanup()
        
        return listings
    except Exception as e:
        logger.error(f"Error in scraping: {str(e)}")
        raise

def handle_db_errors(f):
    """
    Decorator for handling database errors in route handlers.
    Provides consistent error logging and response format.
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
    This endpoint remains unchanged from chat_routes.py.
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
        
        return jsonify({
            'session_id': session_id,
            # 'initial_popup': initial_popup,
            'frontend_message': frontend_message
        }), 201

@chat_bp.route('/complete', methods=['POST'])
@handle_db_errors
def complete_chat():
    """
    Complete the chat session, save preferences, and perform property scraping.
    
    This endpoint extends the basic functionality to include property scraping.
    The main changes are:
    1. Saving final preferences to the database
    2. Performing property scraping based on preferences
    3. Saving scraped properties to the database
    4. Returning property listings in the response
    
    To integrate this functionality:
    1. Replace the complete_chat route in chat_routes.py with this implementation
    2. Ensure the database schema includes the scraped_properties table
    3. Test the scraping functionality before deploying
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

                # Prepare search criteria for scraping
                search_criteria = {
                    'location': session.final_preferences.get('location'),
                    'price_min': session.final_preferences.get('price', {}).get('min'),
                    'price_max': session.final_preferences.get('price', {}).get('max'),
                    'bedrooms_min': session.final_preferences.get('bedrooms', {}).get('min'),
                    'bedrooms_max': session.final_preferences.get('bedrooms', {}).get('max'),
                    'property_type': session.final_preferences.get('propertyType')
                }

                # Run scraping in event loop
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                listings = loop.run_until_complete(perform_scraping(session.session_id, search_criteria))
                loop.close()
                
                return jsonify({
                    'message': 'Chat session completed successfully',
                    'session_id': session.session_id,
                    'property_listings': [listing.to_dict() for listing in listings]
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
#     """
#     # TODO: Implement popup message generation
#     return ""