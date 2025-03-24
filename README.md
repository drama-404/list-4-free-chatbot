# List4Free Chatbot

A full-stack application for a property search chatbot, built with Flask (Python) backend and React frontend.

## Project Structure

```
list-4-free-chatbot/
├── chatbot-backend/     # Flask backend (runs on Windows)
│   ├── models/         # Database models
│   │   └── __init__.py # Makes the directory a Python package
│   ├── routes/         # API routes
│   │   └── __init__.py # Makes the directory a Python package
│   ├── database/       # Database utilities
│   │   └── __init__.py # Makes the directory a Python package
│   ├── app.py         # Main application file
│   ├── config.py      # Configuration settings
│   ├── .env.example   # Example environment variables (commit this)
│   └── .env           # Environment variables (do not commit)
└── chatbot-frontend/   # React frontend (runs on WSL)
    ├── src/           # Source code
    ├── public/        # Static files
    ├── .env.example   # Example environment variables (commit this)
    ├── .env           # Environment variables (do not commit)
    └── package.json   # Dependencies
```

## Prerequisites

- Windows 10/11 with WSL2 installed
- Python 3.8+ (on Windows)
- Node.js 14+ (on WSL)
- PostgreSQL (on Windows)
- pgAdmin 4 (optional, for database management)

## Initial Setup

### Python Package Structure
The backend uses Python packages to organize code. Each directory containing Python modules should have an `__init__.py` file:

1. Create empty `__init__.py` files in these directories:
   ```
   chatbot-backend/models/__init__.py
   chatbot-backend/routes/__init__.py
   chatbot-backend/database/__init__.py
   ```

### Environment Variables
Both frontend and backend use environment variables for configuration. These should never be committed to version control.

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

1. Install PostgreSQL on Windows if not already installed
2. Create a database named `l4f-chatbot-db` in pgAdmin or using psql
3. Configure PostgreSQL to accept connections:
   - Open `postgresql.conf` and set `listen_addresses = '*'`
   - Open `pg_hba.conf` and add:
     ```
     host    all             all             172.16.0.0/12           scram-sha-256
     ```
   - Restart PostgreSQL service

## Backend Setup (Windows)

1. Navigate to the backend directory:
   ```cmd
   cd C:\Users\denad\OneDrive\Desktop\List4Free\list-4-free-chatbot\chatbot-backend
   ```

2. Create and activate virtual environment:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```cmd
   copy .env.example .env
   # Edit .env with your actual values
   ```

5. Run the Flask application:
   ```cmd
   python app.py
   ```

The backend will run on:
- http://127.0.0.1:5000
- http://192.168.1.4:5000

## Frontend Setup (WSL)

1. Open WSL terminal and navigate to the frontend directory:
   ```bash
   cd /mnt/c/Users/denad/OneDrive/Desktop/List4Free/list-4-free-chatbot/chatbot-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env if needed
   ```

4. Start the development server:
   ```bash
   npm start
   ```

The frontend will run on:
- http://localhost:3000

## Development Workflow

1. Keep two terminal windows open:
   - Windows CMD for the backend (port 5000)
   - WSL terminal for the frontend (port 3000)

2. The backend runs on Windows to maintain direct connection with PostgreSQL
3. The frontend runs on WSL for better development experience
4. CORS is configured to allow communication between frontend and backend

## Version Control

1. Never commit `.env` files to version control
2. Always commit `.env.example` files with example values
3. Make sure both `.gitignore` files exclude:
   - Backend: `.env`, `__pycache__/`, `venv/`, etc.
   - Frontend: `.env`, `node_modules/`, `build/`, etc.

## API Endpoints

### Chat Session
- `POST /api/v1/chat/session` - Create new chat session
- `GET /api/v1/chat/session/{session_id}` - Get session details
- `POST /api/v1/chat/session/{session_id}/message` - Send message
- `POST /api/v1/chat/session/{session_id}/preferences` - Set preferences
- `POST /api/v1/chat/session/{session_id}/search` - Perform search

## Troubleshooting

1. Database Connection Issues:
   - Verify PostgreSQL is running on Windows
   - Check if the database exists
   - Verify credentials in `.env` file
   - Ensure PostgreSQL is configured to accept connections

2. Backend Issues:
   - Check if virtual environment is activated
   - Verify all dependencies are installed
   - Check logs for specific error messages
   - Ensure all `__init__.py` files exist

3. Frontend Issues:
   - Verify Node.js version in WSL
   - Check if all dependencies are installed
   - Ensure backend is running and accessible
