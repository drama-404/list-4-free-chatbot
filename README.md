# List4Free Chatbot

A full-stack application for a property search chatbot, built with Flask (Python) backend and React frontend.

## Project Structure

```
list-4-free-chatbot/
├── chatbot-backend/     # Flask backend
│   ├── models/         # Database models
│   ├── routes/         # API routes
│   ├── database/       # Database utilities
│   ├── app.py         # Main application file
│   ├── config.py      # Configuration settings
│   ├── .env.example   # Example environment variables (commit this)
│   └── .env           # Environment variables (do not commit)
└── chatbot-frontend/   # React frontend
    ├── src/           # Source code
    ├── public/        # Static files
    ├── .env.example   # Example environment variables (commit this)
    ├── .env           # Environment variables (do not commit)
    └── package.json   # Dependencies
```

## Prerequisites

- Python 3.8+ 
- Node.js 14+ 
- PostgreSQL 

## Component Documentation

For detailed documentation of each component, please refer to:
- [Backend Documentation](chatbot-backend/README.md)
- [Frontend Documentation](chatbot-frontend/README.md)

## Initial Setup

### Environment Variables
Both frontend and backend use environment variables for configuration. These are not committed to version control.

1. Backend (.env):
   ```bash
   # Create chatbot-backend/.env.example with:
   DB_NAME=l4f-chatbot-db
   DB_USER=postgres
   DB_PASSWORD=your_password_here
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=your-secret-key-here
   FLASK_DEBUG=True
   CORS_ORIGINS=http://localhost:3000

   # Copy to .env and update with real values:
   cp chatbot-backend/.env.example chatbot-backend/.env
   ```

2. Frontend (.env):
   ```bash
   # Create chatbot-frontend/.env.example with:
   REACT_APP_API_URL=http://localhost:5000

   # Copy to .env and update if needed:
   cp chatbot-frontend/.env.example chatbot-frontend/.env
   ```

## Database Setup

You have two options for database setup:

### Option 1: Create New Database
1. Install PostgreSQL if not already installed
2. Create a new database named `l4f-chatbot-db`:
   ```sql
   CREATE DATABASE l4f_chatbot_db;
   ```
3. Run the schema:
   ```bash
   psql -U your_user -d l4f_chatbot_db -f chatbot-backend/database/schema.sql
   ```

### Option 2: Use Existing Database
1. Ensure you have access to the existing PostgreSQL List4Free database
2. Update the database credentials in your `.env` file
3. Run the schema on your existing database:
   ```bash
   psql -U your_user -d your_existing_db -f chatbot-backend/database/schema.sql
   ```

## Development Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd chatbot-backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```bash
   python app.py
   ```

The backend will run on:
- http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd chatbot-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will run on:
- http://localhost:3000

## Development Workflow

1. Keep two terminal windows open:
   - One for the backend (port 5000)
   - One for the frontend (port 3000)

2. Ensure the backend can connect to your PostgreSQL database
3. CORS is configured to allow communication between frontend and backend


