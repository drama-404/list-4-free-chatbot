import React, { useState, useEffect } from 'react';
import ChatWidget from './ChatWidget';
import InitialPopup from './InitialPopup';
import { initiateChat } from '../utils/api';

const ChatContainer = () => {
    const [showChat, setShowChat] = useState(false);
    const [showPopup, setShowPopup] = useState(false);
    const [searchCriteria, setSearchCriteria] = useState(null);
    const [list4freeUserId, setList4freeUserId] = useState(null);
    const [initialResponse, setInitialResponse] = useState(null);
    const [sessionId, setSessionId] = useState(null);

    // Add logging for sessionId
    useEffect(() => {
        console.log('ChatContainer sessionId:', sessionId);
    }, [sessionId]);

    // Function to handle API response
    const handleInitiateResponse = (data) => {
        if (data.frontend_message) {
            setSearchCriteria(data.frontend_message.searchCriteria);
            setList4freeUserId(data.frontend_message.list4freeUserId);
            setSessionId(data.session_id);
            setShowPopup(true);
        }
    };

    // Listen for API responses
    useEffect(() => {
        // Create a function to handle the API response
        const handleApiResponse = async () => {
            try {
                // Make the API call when needed (will trigger this from your main app)
                const response = await initiateChat({
                    location: "London",
                    propertyType: "Residential",
                    propertySubtype: "flat",
                    bedrooms: {
                        min: 2,
                        max: 4
                    },
                    price: {
                        min: 200000,
                        max: 500000
                    }
                }, "user123");

                handleInitiateResponse(response);
            } catch (error) {
                console.error('Error handling API response:', error);
            }
        };

        // For testing purposes
        handleApiResponse();
    }, []);

    const handlePopupResponse = (accepted) => {
        setShowPopup(false);
        if (accepted) {
            setShowChat(true);
            setInitialResponse("Yes, please!");
        }
    };

    return (
        <>
            {showPopup && <InitialPopup onResponse={handlePopupResponse} />}
            {showChat && (
                <ChatWidget
                    initialResponse={initialResponse}
                    searchCriteria={searchCriteria}
                    list4freeUserId={list4freeUserId}
                    sessionId={sessionId}
                />
            )}
        </>
    );
};

export default ChatContainer; 