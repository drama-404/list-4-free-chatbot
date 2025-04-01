# List4Free Chatbot Backend

A Flask-based backend service for the List4Free chatbot, designed to handle chat sessions and property search preferences.

## Features

- Chat session management
- Property search criteria collection
- User preference storage
- Azure PostgreSQL integration
- RESTful API with versioning
- CORS support for frontend integration
- Property scraping from multiple sources (Rightmove, etc.)

## Prerequisites

- Python 3.8+
- PostgreSQL (Azure or local)
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd chatbot-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

Required environment variables:
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `SECRET_KEY`: Flask secret key

Optional environment variables:
- `DB_HOST`: Database host (default: localhost)
- `DB_PORT`: Database port (default: 5433)
- `FLASK_DEBUG`: Enable debug mode (default: False)
- `CORS_ORIGINS`: Allowed origins (default: http://localhost:3000)
- `MAX_SESSION_DURATION`: Session timeout in seconds (default: 3600)
- `MAX_MESSAGES_PER_SESSION`: Message limit per session (default: 100)

## Property Scraping

The backend includes a property scraping module that can fetch listings from various property websites. For detailed information about the scraping functionality, including:

- How to use the scrapers
- How to add new property websites
- Testing the scrapers
- Rate limiting and error handling

See the [Property Scrapers Documentation](scrapers/README.md).

### Quick Start with Property Scraping

```python
from scrapers import ScraperController, RightmoveScraper

# Initialize scrapers
scrapers = [RightmoveScraper()]
controller = ScraperController(scrapers)

# Search for properties
criteria = {
    "location": "London",
    "price_min": 300000,
    "price_max": 500000,
    "bedrooms_min": 2
}

listings = await controller.search(criteria)
```

## Database Setup

1. Create the database:
```bash
psql -U your_user -c "CREATE DATABASE your_db_name;"
```

2. Run the schema:
```bash
psql -U your_user -d your_db_name -f database/schema.sql
```

## Running the Application

Development:
```bash
python app.py
```

Production:
```bash
gunicorn app:app
```

## API Endpoints

### Chat Routes (`/api/v1/chat/`)

#### POST /initiate
Initialize a new chat session.

Request:
```json
{
    "search_criteria": {
        "location": "string",
        "propertyType": "string",
        "bedrooms": {
            "min": 1,
            "max": 5
        },
        "price": {
            "min": 100000,
            "max": 1000000
        }
    },
    "list4free_user_id": "string (optional)"
}
```

Response:
```json
{
    "session_id": "uuid",
    "initial_popup": "string",
    "frontend_message": {
        "type": "INITIATE_CHAT",
        "searchCriteria": {},
        "list4freeUserId": "string"
    }
}
```

#### POST /complete
Complete a chat session.

Request:
```json
{
    "session_id": "uuid",
    "final_preferences": {},
    "user_email": "string (optional)",
    "conversation_summary": []
}
```

Response:
```json
{
    "message": "Chat session completed successfully",
    "session_id": "uuid"
}
```

## Project Structure

```
chatbot-backend/
├── app.py              # Main application entry point
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── database/          # Database utilities and schema
├── models/            # SQLAlchemy models
├── routes/            # API route handlers
└── scrapers/          # Property scraping module
    ├── core/          # Core scraping functionality
    ├── providers/     # Website-specific scrapers
    └── test_scrapers.py  # Test script
```

## Integration with Frontend

The backend is designed to work with the List4Free chatbot frontend:
- CORS is configured for `http://localhost:3000`
- API endpoints are versioned (`/api/v1/`)
- JSON responses follow a consistent format

## Error Handling

- All API endpoints return appropriate HTTP status codes
- Database errors are logged and handled gracefully
- Configuration validation on startup
- CORS errors are prevented with proper headers