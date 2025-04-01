"""
Database Connection Test Module

This module provides utilities for testing the database connection.
Useful for verifying Azure PostgreSQL connection details and permissions.

Note: Schema initialization is handled manually through schema.sql
"""

import os
import logging
from dotenv import load_dotenv
from db_utils import test_connection

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    Test the database connection and log the results.
    Useful for verifying Azure PostgreSQL connection details.
    """
    try:
        logger.info("Testing database connection...")
        if test_connection():
            logger.info("Database connection test completed successfully")
        else:
            logger.error("Database connection test failed")
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        raise

if __name__ == "__main__":
    main() 