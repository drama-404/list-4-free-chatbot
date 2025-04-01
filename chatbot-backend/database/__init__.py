"""
Database Package

This package provides database utilities and schema management for the List4Free chatbot.
It handles database connections, session management, and schema initialization.

Components:
-----------
1. Database Connection
   - Connection pooling
   - Session management
   - Error handling

2. Schema Management
   - Table definitions
   - Index creation
   - Constraint management

3. Utility Functions
   - Connection testing
   - Session cleanup
   - Error logging

Usage:
------
from database import get_db, init_db

# Initialize database connection
init_db()

# Use database session
with get_db() as db:
    # Perform database operations
    pass
"""

from .db_utils import (
    DatabaseConnection,
    get_db,
    init_db,
    test_connection
)

__all__ = [
    'DatabaseConnection',
    'get_db',
    'init_db',
    'test_connection'
] 