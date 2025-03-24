# Chatbot API Documentation

## Base URL
```
http://localhost:5000/api/v1/chat
```

## Authentication
All endpoints require the following header:
```
Content-Type: application/json
```

## Endpoints

### 1. Initialize Chat Session
Creates a new chat session when the main app's search yields no results.

**Endpoint:** `POST /initiate`

**Request Body:**
```json
{
    "search_criteria": {
        "location": "string or null",
        "propertyType": "string or null",
        "propertySubtype": "string or null",
        "bedrooms": {
            "min": "integer or null",
            "max": "integer or null"
        },
        "price": {
            "min": "integer or null",
            "max": "integer or null"
        }
    },
    "list4free_user_id": "string or null"
}
```

**Response (201 Created):**
```json
{
    "session_id": "uuid-string",
    "initial_popup": "string"
}
```

**Error Responses:**
- 400 Bad Request: If search criteria is missing or invalid
- 500 Internal Server Error: For database errors

**Postman Example:**
1. Create a new request
2. Set method to `POST`
3. Enter URL: `http://localhost:5000/api/chat/initiate`
4. Set Headers:
   - `Content-Type: application/json`
5. Set Body (raw JSON):
   ```json
   {
       "search_criteria": {
           "location": "London",
           "propertyType": "House",
           "propertySubtype": "Detached",
           "bedrooms": {
               "min": 2,
               "max": 4
           },
           "price": {
               "min": 200000,
               "max": 500000
           }
       },
       "list4free_user_id": "user123"  // Optional
   }
   ```
6. Send request

### 2. Complete Chat Session
Finalizes the chat session and sends data back to the main app.

**Endpoint:** `POST /complete`

**Request Body:**
```json
{
    "session_id": "uuid-string",
    "final_preferences": {
        "location": "string or null",
        "propertyType": "string or null",
        "propertySubtype": "string or null",
        "bedrooms": {
            "min": "integer or null",
            "max": "integer or null"
        },
        "price": {
            "min": "integer or null",
            "max": "integer or null"
        },
        "hasPublicTransport": "boolean or null",
        "hasSchools": "boolean or null",
        "timeline": "string or null",
        "hasPreApprovedLoan": "boolean or null"
    },
    "user_email": "string (optional)",
    "conversation_summary": "json format of the entire conversation"
}
```

**Response (200 OK):**
```json
{
    "message": "Chat session completed successfully",
    "main_app_search_id": "string"
}
```

**Error Responses:**
- 400 Bad Request: If session_id or final_preferences is missing or invalid
- 404 Not Found: If session doesn't exist
- 500 Internal Server Error: For database errors

**Postman Example:**
1. Create a new request
2. Set method to `POST`
3. Enter URL: `http://localhost:5000/api/chat/complete`
4. Set Headers:
   - `Content-Type: application/json`
5. Set Body (raw JSON):
   ```json
   {
       "session_id": "550e8400-e29b-41d4-a716-446655440000",
       "final_preferences": {
           "location": "London",
           "propertyType": "House",
           "propertySubtype": "Detached",
           "bedrooms": {
               "min": 3,
               "max": 4
           },
           "price": {
               "min": 250000,
               "max": 450000
           },
           "hasPublicTransport": true,
           "hasSchools": true,
           "timeline": "within_3_months",
           "hasPreApprovedLoan": true
       },
       "user_email": "user@example.com",  // Optional
       "conversation_summary": {
           "messages": [
               {
                   "type": "bot",
                   "content": "I see you're looking for a House in London...",
                   "timestamp": "2024-03-24T14:30:00.000Z"
               },
               {
                   "type": "user",
                   "content": "Yes, I'd like to modify the criteria",
                   "timestamp": "2024-03-24T14:31:00.000Z"
               }
           ]
       }
   }
   ```
6. Send request

## Important Notes

### General
- All timestamps are in UTC
- The chatbot maintains conversation state in the frontend
- No API calls are made during the conversation
- Data is only saved to the database at the beginning and end of the session

### Session Management
- Each chat session has a unique UUID
- Sessions are active by default until explicitly completed
- A session can only be completed once

### Data Storage
- Initial search criteria is stored when the session is created
- Final preferences and conversation summary are stored when the session is completed
- All data is stored in JSON format for flexibility

### Error Handling
- All endpoints return appropriate HTTP status codes
- Error responses include a descriptive message
- Database errors are logged but return a generic 500 error to the client
- Invalid session IDs return a 404 error

### Security
- No authentication is required for the API endpoints
- Consider implementing authentication for production use
- Sensitive data (like user email) is optional and should be handled securely 