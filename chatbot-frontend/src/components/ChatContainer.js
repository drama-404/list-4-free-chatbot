/**
 * ChatContainer Component
 * 
 * A floating chat widget component that appears in the bottom right corner
 * of the main List4Free application when no search results are found.
 * This component is designed to be rendered within the main app's UI
 * without affecting its layout or background.
 * 
 * Props:
 * @param {Object} searchCriteria - Search criteria from the main app
 * @param {string} list4freeUserId - User ID from the main app if logged in
 * @param {string} sessionId - Session ID from the initiateChat API call
 * 
 * Integration Points:
 * 1. Main App Integration:
 *    - Render this component directly in your search results page
 *    - Do NOT render the entire App component
 *    - The component will float in the bottom right corner
 *    - The main app's UI and background will remain unchanged
 * 
 * 2. State Management:
 *    - Manages visibility of chat widget and initial popup
 *    - Handles search criteria and user identification
 *    - Maintains session ID for chat completion
 * 
 * 3. User Flow:
 *    Initial Popup -> Chat Widget -> Chat Completion
 * 
 * Usage in Main App:
 * ```jsx
 * // In your search results component
 * const SearchResults = () => {
 *   const [results, setResults] = useState([]);
 *   const [searchCriteria, setSearchCriteria] = useState(null);
 *   const [userId, setUserId] = useState(null);
 *   
 *   useEffect(() => {
 *     if (results.length === 0) {
 *       // Get search criteria from your search form/state
 *       const criteria = {
 *         location: searchForm.location,
 *         propertyType: searchForm.propertyType,
 *         // ... other search criteria
 *       };
 *       
 *       // Get user ID if logged in
 *       const currentUserId = isLoggedIn ? currentUser.id : null;
 *       
 *       setSearchCriteria(criteria);
 *       setUserId(currentUserId);
 *     }
 *   }, [results]);
 *   
 *   return (
 *     <>
 *       {// Your existing search results UI //}
 *       {results.length === 0 && (
 *         <ChatContainer 
 *           searchCriteria={searchCriteria}
 *           list4freeUserId={userId}
 *         />
 *       )}
 *     </>
 *   );
 * };
 * ```
 * 
 * Note: This component is styled to float in the bottom right corner
 * and will not affect the layout of your main application.
 */

import React, { useState } from 'react';
import ChatWidget from './ChatWidget';
import InitialPopup from './InitialPopup';

const ChatContainer = ({ searchCriteria, list4freeUserId, sessionId }) => {
    // State management for UI visibility
    const [showChat, setShowChat] = useState(false);
    const [showPopup, setShowPopup] = useState(false);
    const [initialResponse, setInitialResponse] = useState(null);

    /**
     * Handles the user's response to the initial popup
     * Shows the chat widget if the user accepts
     * 
     * @param {boolean} accepted - Whether the user accepted the chat
     */
    const handlePopupResponse = (accepted) => {
        setShowPopup(false);
        if (accepted) {
            setShowChat(true);
            setInitialResponse("Yes, please!");
        }
    };

    // Show popup when search criteria is available
    if (searchCriteria && !showPopup && !showChat) {
        setShowPopup(true);
    }

    // Render components based on state
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