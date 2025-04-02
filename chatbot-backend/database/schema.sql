/*
 * List4Free Chatbot Database Schema
 * 
 * INTEGRATION NOTES:
 * -----------------
 * 1. This schema can be integrated into the existing Azure PostgreSQL database
 * 2. Execute this script manually to add chatbot functionality
 * 3. The tables are designed to work independently and won't interfere with existing tables
 * 4. Adjust the VARCHAR lengths if needed to match the main app's conventions
 */

-- -- Create users  -> Similar table is already present in the main app's database
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


-- Create scraped_properties table
CREATE TABLE IF NOT EXISTS scraped_properties (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(session_id),
    listing_id VARCHAR(255) NOT NULL,
    source VARCHAR(50) NOT NULL,
    url TEXT NOT NULL,
    title VARCHAR(255),
    description TEXT,
    address TEXT,
    city VARCHAR(100),
    postcode VARCHAR(20),
    region VARCHAR(100),
    country VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    bedrooms INTEGER,
    bathrooms INTEGER,
    reception_rooms INTEGER,
    property_type VARCHAR(50),
    tenure VARCHAR(50),
    floor_area DECIMAL(10, 2),
    year_built INTEGER,
    features JSONB,
    energy_rating VARCHAR(10),
    council_tax_band VARCHAR(10),
    price_amount DECIMAL(12, 2),
    price_currency VARCHAR(3),
    price_type VARCHAR(50),
    is_under_offer BOOLEAN DEFAULT false,
    is_sold BOOLEAN DEFAULT false,
    sold_date DATE,
    sold_price DECIMAL(12, 2),
    images TEXT[],
    floor_plans TEXT[],
    virtual_tour_url TEXT,
    available_from DATE,
    last_updated TIMESTAMP WITH TIME ZONE,
    agent_name VARCHAR(255),
    agent_company VARCHAR(255),
    agent_phone VARCHAR(50),
    agent_email VARCHAR(255),
    agent_website TEXT,
    raw_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, listing_id)
);

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_scraped_properties_session_id ON scraped_properties(session_id);
CREATE INDEX IF NOT EXISTS idx_scraped_properties_listing_id ON scraped_properties(listing_id);
CREATE INDEX IF NOT EXISTS idx_scraped_properties_source ON scraped_properties(source);

-- Create trigger function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for scraped_properties
CREATE TRIGGER update_scraped_properties_updated_at
    BEFORE UPDATE ON scraped_properties
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();