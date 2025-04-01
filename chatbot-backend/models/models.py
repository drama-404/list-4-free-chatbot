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
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
import uuid
from .base import Base

class ChatSession(Base):
    """
    Chat Session Model
    
    Represents a single chat session between a user and the chatbot.
    Stores all relevant information about the conversation, including
    search criteria, user preferences, and session state.
    
    Attributes:
        id (int): Primary key
        session_id (str): UUID for the session
        list4free_user_id (str): ID of logged-in List4Free user
        user_email (str): User's email address
        created_at (datetime): Session creation timestamp
        closed_at (datetime): Session closure timestamp
        is_active (bool): Whether the session is active
        initial_search_criteria (dict): Initial search parameters
        final_preferences (dict): Confirmed property preferences
        conversation_summary (dict): Summary of the conversation
        main_app_search_id (str): Reference to main app search
    """
    __tablename__ = 'chat_sessions'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    list4free_user_id = Column(String(36), nullable=True)
    user_email = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Store the initial search criteria from main app
    initial_search_criteria = Column(JSON, nullable=False)
    
    # Store the final confirmed preferences
    final_preferences = Column(JSON, nullable=True)
    
    # Store the conversation summary
    conversation_summary = Column(JSON, nullable=True)
    
    # Reference to the main app's search entry
    main_app_search_id = Column(String(36), nullable=True)

    def __repr__(self):
        return f"<ChatSession(session_id='{self.session_id}', is_active={self.is_active})>"