from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, JSON
from sqlalchemy.orm import relationship
import uuid
from .base import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    last_active = Column(DateTime(timezone=True), default=datetime.utcnow)

class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    list4free_user_id = Column(Integer, nullable=True)
    list4free_email = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    last_active = Column(DateTime(timezone=True), default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    property_preferences = relationship("PropertyPreference", back_populates="chat_session")
    chat_messages = relationship("ChatMessage", back_populates="chat_session")
    search_history = relationship("SearchHistory", back_populates="chat_session")
    conversation_state = relationship("ConversationState", back_populates="chat_session", uselist=False)

class PropertyPreference(Base):
    __tablename__ = 'property_preferences'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('chat_sessions.id'))
    location = Column(String(255), nullable=False)
    property_type = Column(String(50), nullable=False)
    property_subtype = Column(String(50))
    min_bedrooms = Column(Integer)
    max_bedrooms = Column(Integer)
    min_price = Column(Numeric(12, 2))
    max_price = Column(Numeric(12, 2))
    has_transport = Column(Boolean, default=False)
    has_school = Column(Boolean, default=False)
    timeline = Column(String(20), nullable=False)
    has_pre_approved_loan = Column(Boolean)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationship
    chat_session = relationship("ChatSession", back_populates="property_preferences")

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('chat_sessions.id'))
    message_type = Column(String(50), nullable=False)  # 'bot' or 'user'
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationship
    chat_session = relationship("ChatSession", back_populates="chat_messages")

class SearchHistory(Base):
    __tablename__ = 'search_history'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('chat_sessions.id'))
    search_criteria = Column(JSON, nullable=False)
    results_count = Column(Integer, default=0)
    is_deep_search = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at = Column(DateTime(timezone=True))
    email_sent = Column(Boolean, default=False)
    email_sent_at = Column(DateTime(timezone=True))
    
    # Relationship
    chat_session = relationship("ChatSession", back_populates="search_history")

class ConversationState(Base):
    __tablename__ = 'conversation_state'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('chat_sessions.id'), unique=True)
    current_step = Column(String(50), nullable=False)
    last_user_input = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationship
    chat_session = relationship("ChatSession", back_populates="conversation_state")
