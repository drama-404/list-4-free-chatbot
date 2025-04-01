/**
 * App Component
 * 
 * This is the root component of the chatbot application.
 * When integrated with the main List4Free application, this file should be replaced
 * with the main app's integration code.
 * 
 * Integration Points:
 * 1. Search Results Integration:
 *    - Only render the ChatContainer component when search results are empty
 *    - Do NOT render the entire App component
 *    - The ChatContainer will appear as a floating widget in the bottom right
 *    - The main app's UI and background will remain unchanged
 * 
 * 2. User Authentication:
 *    - Replace the test user ID with the actual logged-in user's ID
 *    - If no user is logged in, pass null
 * 
 * Example Integration in Main App:
 * ```jsx
 * // In your main app's search results component
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
 *       {// Your existing search results UI }
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
 * Note: The ChatContainer component is styled to float in the bottom right corner
 * and will not affect the layout of the main application.
 */

import React, { useState, useEffect } from 'react';
import ChatContainer from './components/ChatContainer';
import { initiateChat } from './utils/api';
import './styles/App.css';

function App() {
    // State for chat data
    const [searchCriteria, setSearchCriteria] = useState(null);
    const [list4freeUserId, setList4freeUserId] = useState(null);
    const [sessionId, setSessionId] = useState(null);

    /**
     * Effect: Initialize chat with test data
     * 
     * TODO: Replace this effect with actual integration code
     * This is test data for development purposes only.
     */
    useEffect(() => {
        const initializeChat = async () => {
            try {
                // Test search criteria - REPLACE WITH ACTUAL DATA FROM MAIN APP
                const testSearchCriteria = {
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
                };

                // Test user ID - REPLACE WITH ACTUAL USER ID FROM MAIN APP
                const testUserId = "user123";

                const response = await initiateChat(testSearchCriteria, testUserId);
                
                // Update state with response data
                setSearchCriteria(testSearchCriteria);
                setList4freeUserId(testUserId);
                setSessionId(response.session_id);
            } catch (error) {
                console.error('Error initializing chat:', error);
            }
        };

        initializeChat();
    }, []); // Only run once on component mount

    return (
        <div className="App-header">
            <ChatContainer 
                searchCriteria={searchCriteria}
                list4freeUserId={list4freeUserId}
                sessionId={sessionId}
            />
        </div>
    );
}

export default App;
