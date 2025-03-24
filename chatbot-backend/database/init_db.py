import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database():
    """Create the database if it doesn't exist"""
    # Debug logging for environment variables
    logger.info(f"DB_USER: {os.getenv('DB_USER')}")
    logger.info(f"DB_PASSWORD: {'*' * len(os.getenv('DB_PASSWORD', ''))}")  # Mask password
    logger.info(f"DB_HOST: {os.getenv('DB_HOST')}")
    logger.info(f"DB_PORT: {os.getenv('DB_PORT')}")
    logger.info(f"DB_NAME: {os.getenv('DB_NAME')}")

    conn_params = {
        'dbname': 'postgres',
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5433')
    }

    try:
        conn = psycopg2.connect(**conn_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Check if database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'l4f-chatbot-db'")
        exists = cur.fetchone()

        if not exists:
            cur.execute('CREATE DATABASE "l4f-chatbot-db"')
            logger.info("Database 'l4f-chatbot-db' created successfully")
        else:
            logger.info("Database 'l4f-chatbot-db' already exists")

        cur.close()
        conn.close()

    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise

def init_schema():
    """Initialize the database schema"""
    from db_utils import db

    try:
        # Get the absolute path to the schema.sql file
        current_dir = Path(__file__).parent
        schema_path = current_dir / 'schema.sql'

        # Execute the schema script
        db.execute_script(str(schema_path))
        logger.info("Database schema initialized successfully")

    except Exception as e:
        logger.error(f"Error initializing schema: {e}")
        raise

def main():
    """Main function to initialize the database"""
    try:
        logger.info("Starting database initialization...")
        create_database()
        init_schema()
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

if __name__ == "__main__":
    main() 