"""
Database Models Module

This module defines all database models for the List4Free chatbot.
It uses SQLAlchemy's declarative base for model definitions.

Models:
--------
1. ChatSession
   - Stores chat session information
   - Links to List4Free user (if logged in)
   - Stores search criteria and preferences
   - Manages conversation state
   - Stores conversation summary as JSON

Integration Points:
------------------
1. Database:
   - Uses SQLAlchemy ORM
   - Supports PostgreSQL
   - Handles JSON fields for flexible data storage

2. Frontend:
   - Provides data structure for API responses
   - Manages chat session state
   - Handles user preferences
   - Manages conversation flow in memory

3. Main Application:
   - Links to List4Free user accounts
   - Integrates with search functionality
   - Manages property preferences
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey, Numeric, ARRAY, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from .base import Base
     

class ChatSession(Base):
    """
    Chat Session Model
    
    Represents a single chat session between a user and the chatbot.
    Stores all relevant information about the conversation, including
    search criteria, user preferences, and session state.
    
    Attributes:
        session_id (UUID): Primary key
        list4free_user_id (str): ID of logged-in List4Free user
        initial_search_criteria (JSONB): Initial search parameters
        final_preferences (JSONB): Confirmed property preferences
        user_email (str): User's email address
        conversation_summary (String): Summary of the conversation
        is_active (bool): Whether the session is active
        created_at (DateTime): Session creation timestamp
        closed_at (DateTime): Session closure timestamp
    """
    __tablename__ = 'chat_sessions'
    
    session_id = Column(UUID(as_uuid=True), primary_key=True)
    list4free_user_id = Column(String(255))
    initial_search_criteria = Column(JSONB, nullable=False)
    final_preferences = Column(JSONB)
    user_email = Column(String(255))
    conversation_summary = Column(JSONB)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    closed_at = Column(DateTime(timezone=True))

    # Relationship with scraped properties
    scraped_properties = relationship("ScrapedProperty", back_populates="chat_session")

    def __repr__(self):
        return f"<ChatSession(session_id='{self.session_id}', is_active={self.is_active})>"

class ScrapedProperty(Base):
    __tablename__ = 'scraped_properties'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey('chat_sessions.session_id'))
    listing_id = Column(String(255), nullable=False)
    source = Column(String(50), nullable=False)
    url = Column(String, nullable=False)
    title = Column(String(255))
    description = Column(String)
    address = Column(String)
    city = Column(String(100))
    postcode = Column(String(20))
    region = Column(String(100))
    country = Column(String(100))
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    reception_rooms = Column(Integer)
    property_type = Column(String(50))
    tenure = Column(String(50))
    floor_area = Column(Numeric(10, 2))
    year_built = Column(Integer)
    features = Column(JSONB)
    energy_rating = Column(String(10))
    council_tax_band = Column(String(10))
    price_amount = Column(Numeric(12, 2))
    price_currency = Column(String(3))
    price_type = Column(String(50))
    is_under_offer = Column(Boolean, default=False)
    is_sold = Column(Boolean, default=False)
    sold_date = Column(Date)
    sold_price = Column(Numeric(12, 2))
    images = Column(ARRAY(String))
    floor_plans = Column(ARRAY(String))
    virtual_tour_url = Column(String)
    available_from = Column(Date)
    last_updated = Column(DateTime(timezone=True))
    agent_name = Column(String(255))
    agent_company = Column(String(255))
    agent_phone = Column(String(50))
    agent_email = Column(String(255))
    agent_website = Column(String)
    raw_data = Column(JSONB)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with chat session
    chat_session = relationship("ChatSession", back_populates="scraped_properties")

    def to_dict(self):
        """Convert the model to a dictionary."""
        return {
            'id': self.id,
            'session_id': str(self.session_id),
            'listing_id': self.listing_id,
            'source': self.source,
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'location': {
                'address': self.address,
                'city': self.city,
                'postcode': self.postcode,
                'region': self.region,
                'country': self.country,
                'latitude': float(self.latitude) if self.latitude else None,
                'longitude': float(self.longitude) if self.longitude else None
            },
            'features': {
                'bedrooms': self.bedrooms,
                'bathrooms': self.bathrooms,
                'reception_rooms': self.reception_rooms,
                'property_type': self.property_type,
                'tenure': self.tenure,
                'floor_area': float(self.floor_area) if self.floor_area else None,
                'year_built': self.year_built,
                'features': self.features,
                'energy_rating': self.energy_rating,
                'council_tax_band': self.council_tax_band
            },
            'price': {
                'amount': float(self.price_amount) if self.price_amount else None,
                'currency': self.price_currency,
                'price_type': self.price_type,
                'is_under_offer': self.is_under_offer,
                'is_sold': self.is_sold,
                'sold_date': self.sold_date.isoformat() if self.sold_date else None,
                'sold_price': float(self.sold_price) if self.sold_price else None
            },
            'media': {
                'images': self.images,
                'floor_plans': self.floor_plans,
                'virtual_tour_url': self.virtual_tour_url
            },
            'availability': {
                'available_from': self.available_from.isoformat() if self.available_from else None,
                'last_updated': self.last_updated.isoformat() if self.last_updated else None
            },
            'agent': {
                'name': self.agent_name,
                'company': self.agent_company,
                'phone': self.agent_phone,
                'email': self.agent_email,
                'website': self.agent_website
            },
            'raw_data': self.raw_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }