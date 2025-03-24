-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create chat_sessions table
CREATE TABLE chat_sessions (
    id SERIAL PRIMARY KEY,
    session_id UUID NOT NULL,
    list4free_user_id INTEGER, -- NULL for non-logged in users
    list4free_email VARCHAR(255), -- NULL for non-logged in users
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    UNIQUE(session_id)
);

-- Create property_preferences table
CREATE TABLE property_preferences (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES chat_sessions(id),
    location VARCHAR(255) NOT NULL,
    property_type VARCHAR(50) NOT NULL,
    property_subtype VARCHAR(50), -- For residential: studio, flat, detached house, etc.
    min_bedrooms INTEGER,
    max_bedrooms INTEGER,
    min_price DECIMAL(12,2),
    max_price DECIMAL(12,2),
    has_transport BOOLEAN DEFAULT false,
    has_school BOOLEAN DEFAULT false,
    timeline VARCHAR(20) NOT NULL, -- 'ASAP', '1-3 months', '3-6 months', 'Not sure yet'
    has_pre_approved_loan BOOLEAN, -- NULL if not asked or user chose not to share
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create chat_messages table
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES chat_sessions(id),
    message_type VARCHAR(50) NOT NULL, -- 'bot' or 'user'
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create search_history table
CREATE TABLE search_history (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES chat_sessions(id),
    search_criteria JSONB NOT NULL,
    results_count INTEGER DEFAULT 0,
    is_deep_search BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    email_sent BOOLEAN DEFAULT false,
    email_sent_at TIMESTAMP WITH TIME ZONE
);

-- Create conversation_state table to track the current state of each chat session
CREATE TABLE conversation_state (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES chat_sessions(id),
    current_step VARCHAR(50) NOT NULL, -- 'initial_popup', 'confirm_criteria', 'location', 'property_type', etc.
    last_user_input TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_chat_sessions_session_id ON chat_sessions(session_id);
CREATE INDEX idx_chat_sessions_list4free_user_id ON chat_sessions(list4free_user_id);
CREATE INDEX idx_property_preferences_session_id ON property_preferences(session_id);
CREATE INDEX idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX idx_search_history_session_id ON search_history(session_id);
CREATE INDEX idx_conversation_state_session_id ON conversation_state(session_id);

-- Create function to update last_active timestamp
CREATE OR REPLACE FUNCTION update_last_active()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_active = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for last_active updates
CREATE TRIGGER update_chat_sessions_last_active
    BEFORE UPDATE ON chat_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_last_active();

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at updates
CREATE TRIGGER update_property_preferences_updated_at
    BEFORE UPDATE ON property_preferences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_conversation_state_updated_at
    BEFORE UPDATE ON conversation_state
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at(); 