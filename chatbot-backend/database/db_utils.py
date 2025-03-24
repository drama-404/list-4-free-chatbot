import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from config import Config
from models.base import Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    _instance = None
    _engine = None
    _Session = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._engine is None:
            self._engine = create_engine(Config.get_database_url())
            self._Session = sessionmaker(bind=self._engine)

    @property
    def engine(self):
        return self._engine

    @property
    def session(self):
        return self._Session()

@contextmanager
def get_db():
    """Provide a transactional scope around a series of operations"""
    db = DatabaseConnection()
    session = db.session
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()

def create_database():
    """Create the database if it doesn't exist"""
    # Connect to default PostgreSQL database
    default_url = f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/postgres"
    engine = create_engine(default_url)
    
    try:
        with engine.connect() as conn:
            # Check if database exists
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{Config.DB_NAME}'"))
            if not result.scalar():
                # Create database
                conn.execute(text(f"CREATE DATABASE {Config.DB_NAME}"))
                logger.info(f"Database {Config.DB_NAME} created successfully")
            else:
                logger.info(f"Database {Config.DB_NAME} already exists")
    except SQLAlchemyError as e:
        logger.error(f"Error creating database: {str(e)}")
        raise

def init_db(create_schema=False):
    """Initialize database connection and optionally create schema"""
    try:
        # Create database if it doesn't exist
        create_database()
        
        # Create engine for our database
        engine = create_engine(Config.get_database_url())
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            logger.info("Database connection successful")
        
        if create_schema:
            # Create all tables
            Base.metadata.create_all(bind=engine)
            logger.info("Database schema created successfully")
        
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

# Create singleton instance
db = DatabaseConnection()

# Example usage:
"""
# Query example
results = db.execute_query(
    "SELECT * FROM users WHERE email = %s",
    ('user@example.com',)
)

# Batch insert example
db.execute_many(
    "INSERT INTO chat_messages (session_id, message_type, content) VALUES (%s, %s, %s)",
    [(1, 'bot', 'Hello'), (1, 'user', 'Hi')]
)

# Script execution example
db.execute_script('path/to/schema.sql')
""" 