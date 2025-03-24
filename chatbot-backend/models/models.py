from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, JSON
from sqlalchemy.orm import relationship
import uuid
from .base import Base

class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(36), unique=True, nullable=False)  # UUID
    list4free_user_id = Column(String(36), nullable=True)  # Only if user is logged in
    user_email = Column(String(255), nullable=True)  # Collected during chat
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
    
    # Relationship
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('chat_sessions.id'))
    message_type = Column(String(10), nullable=False)  # 'user' or 'bot'
    content = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("ChatSession", back_populates="messages")

# # Commented out unnecessary models for now

# class User(Base):
#     __tablename__ = 'users'
    
#     id = Column(Integer, primary_key=True)
#     email = Column(String(255), unique=True, nullable=False)
#     created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
#     last_active = Column(DateTime(timezone=True), default=datetime.utcnow)

# class PropertyPreference(Base):
#     __tablename__ = 'property_preferences'
    
#     id = Column(Integer, primary_key=True)
#     session_id = Column(Integer, ForeignKey('chat_sessions.id'))
#     location = Column(String(255), nullable=False)
#     property_type = Column(String(50), nullable=False)
#     property_subtype = Column(String(50))
#     min_bedrooms = Column(Integer)
#     max_bedrooms = Column(Integer)
#     min_price = Column(Numeric(12, 2))
#     max_price = Column(Numeric(12, 2))
#     has_transport = Column(Boolean, default=False)
#     has_school = Column(Boolean, default=False)
#     timeline = Column(String(20), nullable=False)
#     has_pre_approved_loan = Column(Boolean)
#     created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
#     updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
#     chat_session = relationship("ChatSession", back_populates="property_preferences")

# class SearchHistory(Base):
#     __tablename__ = 'search_history'
    
#     id = Column(Integer, primary_key=True)
#     session_id = Column(Integer, ForeignKey('chat_sessions.id'))
#     search_criteria = Column(JSON, nullable=False)
#     results_count = Column(Integer, default=0)
#     is_deep_search = Column(Boolean, default=False)
#     created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
#     completed_at = Column(DateTime(timezone=True))
#     email_sent = Column(Boolean, default=False)
#     email_sent_at = Column(DateTime(timezone=True))
    
#     chat_session = relationship("ChatSession", back_populates="search_history")

# class ConversationState(Base):
#     __tablename__ = 'conversation_state'
    
#     id = Column(Integer, primary_key=True)
#     session_id = Column(Integer, ForeignKey('chat_sessions.id'), unique=True)
#     current_step = Column(String(50), nullable=False)
#     last_user_input = Column(String)
#     created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
#     updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
#     chat_session = relationship("ChatSession", back_populates="conversation_state")
