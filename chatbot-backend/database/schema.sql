/*
 * List4Free Chatbot Database Schema
 * 
 * INTEGRATION NOTES:
 * -----------------
 * 1. This schema can be integrated into the existing Azure PostgreSQL database
 * 2. Execute this script manually to add chatbot functionality
 * 3. The chat_sessions table is designed to work independently and won't interfere with existing tables
 * 4. Adjust the VARCHAR lengths if needed to match the main app's conventions
 */

-- -- Create users  -> This is already present in the main app's database
-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     email VARCHAR(255) UNIQUE NOT NULL,
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
--     last_active TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
-- );

-- Create chat_sessions table
-- This table stores all chatbot interactions, including both logged-in and anonymous users
CREATE TABLE chat_sessions (
    -- Primary key and session identifier
    id SERIAL PRIMARY KEY,
    session_id UUID NOT NULL,
    
    -- User identification (can be linked to your main app's user system)
    list4free_user_id VARCHAR(36),     -- NULL for non-logged in users
                                       -- Adjust length to match your user ID format
    user_email VARCHAR(255),           -- Collected during chat
                                       -- Adjust length to match your email field convention
    
    -- Timestamps for session management
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP WITH TIME ZONE, -- When the chat session ends
    is_active BOOLEAN DEFAULT true,     -- Indicates if session is still active
    
    -- Search criteria and preferences
    initial_search_criteria JSONB NOT NULL, -- Initial search parameters that yielded no results
    final_preferences JSONB,               -- Final preferences after chat completion
    conversation_summary JSONB,            -- Summary of the chat conversation
    
    -- Integration with main application
    main_app_search_id VARCHAR(36),        -- Optional: Link to main app's search functionality
                                          -- Adjust length to match your search ID format
    
    -- Ensure unique session IDs
    UNIQUE(session_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_chat_sessions_session_id ON chat_sessions(session_id);
CREATE INDEX idx_chat_sessions_list4free_user_id ON chat_sessions(list4free_user_id);
CREATE INDEX idx_chat_sessions_user_email ON chat_sessions(user_email);