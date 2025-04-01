"""
Database Utilities Module

This module provides database connection and session management for the List4Free chatbot.
It uses SQLAlchemy for database operations and implements a singleton pattern for connection management.

Integration Points:
1. Azure PostgreSQL:
   - Uses environment variables for connection details
   - Supports connection pooling for better performance
   - Handles connection errors gracefully

2. Main Application:
   - Can be integrated with the main app's database
   - Uses the same connection pool for all operations
   - Maintains transaction integrity

Example Usage:
-------------
1. Basic Query:
    with get_db() as db:
        result = db.query(YourModel).filter_by(id=1).first()

2. Transaction with Error Handling:
    try:
        with get_db() as db:
            # Your database operations
            db.add(new_record)
            db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Database operation failed: {str(e)}")
        raise

3. Connection Testing:
    if test_connection():
        print("Database connection is working")
"""

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
    """
    Singleton class for managing database connections.
    Ensures only one connection pool is created and reused.
    """
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
        """Get the SQLAlchemy engine instance"""
        return self._engine

    @property
    def session(self):
        """Get a new database session"""
        return self._Session()

@contextmanager
def get_db():
    """
    Context manager for database sessions.
    Provides automatic transaction management and cleanup.
    
    Usage:
        with get_db() as db:
            # Your database operations here
            db.query(...)
    
    The session will be automatically committed if no errors occur,
    or rolled back if an error is raised.
    """
    db = DatabaseConnection()
    session = db.session
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error: {str(e)}")
        raise e
    finally:
        session.close()

def test_connection():
    """
    Test the database connection.
    Useful for verifying connection details and permissions.
    
    Returns:
        bool: True if connection is successful, raises exception otherwise
    """
    try:
        db = DatabaseConnection()
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            logger.info("Database connection test successful")
            return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection test failed: {str(e)}")
        raise

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