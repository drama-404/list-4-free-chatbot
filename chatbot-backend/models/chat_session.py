from datetime import datetime
from services.database import db
import uuid

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.UUID, default=uuid.uuid4, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')

    search_filters = db.relationship('SearchFilter', backref='chat_session', lazy=True)
    user_contacts = db.relationship('UserContact', backref='chat_session', lazy=True)