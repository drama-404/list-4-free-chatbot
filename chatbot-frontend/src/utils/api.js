/**
 * API Utility Module
 * 
 * Handles all API interactions with the backend server.
 * Provides functions for initiating and completing chat sessions.
 * 
 * Environment Variables:
 * - REACT_APP_API_URL: Base URL for the API
 */

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api/v1';

/**
 * Initiates a new chat session with the backend
 * 
 * @param {Object} searchCriteria - The search criteria from the main app
 * @param {string} [list4freeUserId=null] - user ID from the main app if the user is logged in
 * @returns {Promise<Object>} Response from the backend containing new session details
 * @throws {Error} If the API request fails
 */
export const initiateChat = async (searchCriteria, list4freeUserId = null) => {
    try {
        console.log('Making API call to:', `${API_URL}/chat/initiate`);
        const response = await fetch(`${API_URL}/chat/initiate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                search_criteria: searchCriteria,
                list4free_user_id: list4freeUserId
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error initiating chat:', error);
        throw error;
    }
};

/**
 * Completes a chat session and sends final preferences to the backend
 * 
 * @param {string} sessionId - The unique identifier for the chat session
 * @param {Object} finalPreferences - The final property preferences from the chat
 * @param {string} [userEmail=null] - Optional user's email address
 * @param {Array} conversationSummary - Summary of the chat conversation
 * @returns {Promise<Object>} Response from the backend confirming completion
 * @throws {Error} If the API request fails
 */
export const completeChat = async (sessionId, finalPreferences, userEmail = null, conversationSummary) => {
    try {
        const requestBody = {
            session_id: sessionId,
            final_preferences: finalPreferences,
            user_email: userEmail,
            conversation_summary: conversationSummary
        };

        console.log('Complete chat request body:', JSON.stringify(requestBody, null, 2));

        const response = await fetch(`${API_URL}/chat/complete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });

        console.log('Response status:', response.status);
        const responseData = await response.json();
        console.log('Response data:', responseData);

        if (!response.ok) {
            throw new Error(responseData.error || `HTTP error! status: ${response.status}`);
        }

        return responseData;
    } catch (error) {
        console.error('Error in completeChat:', error);
        throw error;
    }
};