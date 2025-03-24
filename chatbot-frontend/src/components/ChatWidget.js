import React, { useState, useReducer, useEffect, useRef } from 'react';
import TypingIndicator from './TypingIndicator';
import { CONVERSATION_STATES, PROPERTY_TYPES, TIMELINE_OPTIONS, initialState, extractBedroomNumbers } from '../utils/conversationState';
import { initiateChat, completeChat } from '../utils/api';
import MinimizedChat from './MinimizedChat';
import '../styles/ChatWidget.css';

const conversationReducer = (state, action) => {
    switch (action.type) {
        case 'UPDATE_STATE':
            return { ...state, currentState: action.payload };
        case 'UPDATE_FILTERS':
            return { ...state, filters: { ...state.filters, ...action.payload } };
        case 'UPDATE_PREFERENCES':
            return { ...state, preferences: { ...state.preferences, ...action.payload } };
        case 'SET_EMAIL':
            return { ...state, userEmail: action.payload };
        default:
            return state;
    }
};

const ChatWidget = ({ initialResponse, searchCriteria, list4freeUserId }) => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [state, dispatch] = useReducer(conversationReducer, initialState);
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const chatLogRef = useRef(null);
  const inputRef = useRef(null);
  const [inputError, setInputError] = useState('');
  const [lastActiveMessageId, setLastActiveMessageId] = useState(null);

  const API_URL = process.env.REACT_APP_API_URL;
  const CHAT_API_URL = process.env.REACT_APP_CHAT_API_URL;

    //   const getInitialMessage = () => ({
    //     sender: 'bot',
    //     text: "Looks like there aren't any properties matching your search. Would you like us to conduct a deeper search on the web?",
    //     options: ["Yes, please!", "No, thanks."]
    //   });


    const simulateTyping = () => {
        setIsTyping(true);
        return new Promise(resolve => {
            setTimeout(() => {
                setIsTyping(false);
                resolve();
            }, 1000);
        });
    };

    const validateInput = (input, type) => {
        switch (type) {
            case 'email':
                const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
                return emailRegex.test(input);

            case 'location':
                return input && input.trim().length >= 3;

            case 'bedrooms':
                const number = parseInt(input);
                return !isNaN(number) && number >= 0 && number <= 10;

            default:
                return true;
        }
    };

    const handleUserResponse = async (input) => {
        switch (state.currentState) {
            case CONVERSATION_STATES.INITIAL:
                if (input === "Yes, please!") {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.CONFIRM_FILTERS });
                    
                    // Check if there are existing filters
                    if (state.filters.existingFilters) {
                        // When we have filters from the search
                        return {
                            sender: 'bot',
                            text: `Just to confirm, you're looking for a ${state.filters.propertyType || '[property type]'} in ${state.filters.location || '[location]'} under ${state.filters.price || '[price]'}? Do you want to refine these details?`,
                            options: ["Confirm", "Edit"]
                        };
                    } else {
                        // When no filters exist
                        dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.EDIT_LOCATION });
                        return {
                            sender: 'bot',
                            text: "Please enter your preferred location.",
                            options: null
                        };
                    }
                } else {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.COMPLETED });
                    return {
                        sender: 'bot',
                        text: "Thank you for your time. Feel free to come back if you change your mind!"
                    };
                }

            case CONVERSATION_STATES.CONFIRM_FILTERS:
                if (input === "Confirm") {
                    // If user confirms existing filters, skip to public transport
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.PUBLIC_TRANSPORT });
                    return {
                        sender: 'bot',
                        text: "Do you need public transport close to your property?",
                        options: ["Yes", "No"]
                    };
                } else if (input === "Edit") {
                    // If user wants to edit, start with location
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.EDIT_LOCATION });
                    return {
                        sender: 'bot',
                        text: "Please enter your preferred location.",
                        options: null
                    };
                }
                break;

            case CONVERSATION_STATES.EDIT_LOCATION:
                dispatch({ 
                    type: 'UPDATE_FILTERS', 
                    payload: { location: input } 
                });
                dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.PROPERTY_TYPE });
                return {
                    sender: 'bot',
                    text: "What type of property are you looking for?",
                    options: Object.values(PROPERTY_TYPES).map(type => 
                        typeof type === 'string' ? type : type.label
                    )
                };

            case CONVERSATION_STATES.PROPERTY_TYPE:
                dispatch({ 
                    type: 'UPDATE_FILTERS', 
                    payload: { propertyType: input } 
                });
                
                if (input === "Residential") {
                    const questionId = Date.now();
                    const hintId = questionId + 1;
                    setLastActiveMessageId(questionId);
                    
                    setMessages(prev => [...prev, {
                        sender: 'bot',
                        text: "How many bedrooms are you looking for?",
                        options: null,
                        id: questionId
                    }, {
                        sender: 'bot',
                        text: "You can specify:\n• A single number (e.g., '3')\n• A range (e.g., '2-4' or '2 to 4')\n• Min/max (e.g., 'min 2' or 'max 4')\n• 'No min' or 'No max' for open-ended ranges\n• 'Studio' for 0 bedrooms",
                        isHint: true,
                        id: hintId
                    }]);
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.BEDROOMS });
                    return null;
                } else {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.PUBLIC_TRANSPORT });
                    return {
                        sender: 'bot',
                        text: "Do you need public transport close to your property?",
                        options: ["Yes", "No"]
                    };
                }

            case CONVERSATION_STATES.BEDROOMS:
                const { min, max } = extractBedroomNumbers(input);
                
                // Format the bedroom confirmation message
                let bedroomConfirmation = "";
                if (min === 0 && max === 0) {
                    bedroomConfirmation = "a studio flat";
                } else if (min === null && max !== null) {
                    bedroomConfirmation = `properties with up to ${max} bedroom${max !== 1 ? 's' : ''}`;
                } else if (min !== null && max === null) {
                    bedroomConfirmation = `properties with ${min} or more bedroom${min !== 1 ? 's' : ''}`;
                } else if (min === max) {
                    bedroomConfirmation = `a ${min}-bedroom property`;
                } else {
                    bedroomConfirmation = `properties with ${min} to ${max} bedrooms`;
                }

                dispatch({ 
                    type: 'UPDATE_FILTERS', 
                    payload: { bedrooms: { min, max } } 
                });

                const confirmMessageId = Date.now();
                const optionsMessageId = confirmMessageId + 1;
                setLastActiveMessageId(optionsMessageId);

                setMessages(prev => [...prev, {
                    sender: 'bot',
                    text: `Got it! Looking for ${bedroomConfirmation}.`,
                    id: confirmMessageId
                }, {
                    sender: 'bot',
                    text: "Do you need public transport close to your property?",
                    options: ["Yes", "No"],
                    id: optionsMessageId
                }]);

                dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.PUBLIC_TRANSPORT });
                return null;

            case CONVERSATION_STATES.PUBLIC_TRANSPORT:
                dispatch({
                    type: 'UPDATE_PREFERENCES',
                    payload: { publicTransport: input === "Yes" }
                });
                dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.SCHOOLS });
                return {
                    sender: 'bot',
                    text: "Do you need any schools close to your property?",
                    options: ["Yes", "No"]
                };

            case CONVERSATION_STATES.SCHOOLS:
                dispatch({
                    type: 'UPDATE_PREFERENCES',
                    payload: { schools: input === "Yes" }
                });
                dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.TIMELINE });
                return {
                    sender: 'bot',
                    text: "When do you ideally plan to complete the purchase?",
                    options: ["ASAP", "1-3 months", "3-6 months", "Not sure yet"]
                };

            case CONVERSATION_STATES.TIMELINE:
                dispatch({ 
                    type: 'UPDATE_PREFERENCES', 
                    payload: { timeline: input } 
                });
                
                if (input === "ASAP") {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.FINANCIAL_READINESS });
                    return {
                        sender: 'bot',
                        text: "We would offer you a special treatment in case you have a pre-approved loan agreement. Do you have one?",
                        options: ["Yes", "No", "Don't prefer to share these details"]
                    };
                } else {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.EMAIL_REQUEST });
                    setMessages(prev => [...prev, {
                        sender: 'bot',
                        text: "Please note that you may be requested to show a Pre-Approved Loan Agreement before the viewing of a property.",
                        isHint: true,
                        id: Date.now()
                    }, {
                        sender: 'bot',
                        text: "Please leave with us your email address and we'll come back to you within 2 hours.",
                        id: Date.now() + 1
                    }]);
                    return null;
                }

            case CONVERSATION_STATES.FINANCIAL_READINESS:
                if (input === "Yes") {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.COMPLETED });
                    const hintId = Date.now();
                    const finalMessageId = hintId + 1;
                    setLastActiveMessageId(finalMessageId);

                    setMessages(prev => [...prev, {
                        sender: 'bot',
                        text: "Please note that you may be requested to show a Pre-Approved Loan Agreement before the viewing of a property.",
                        isHint: true,
                        id: hintId
                    }, {
                        sender: 'bot',
                        text: "Please register an account and we shall provide all the available properties that match your requirements.",
                        options: ["Register"],
                        id: finalMessageId
                    }]);
                    return null;
                } else {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.EMAIL_REQUEST });
                    setMessages(prev => [...prev, {
                        sender: 'bot',
                        text: "Please note that you may be requested to show a Pre-Approved Loan Agreement before the viewing of a property.",
                        isHint: true,
                        id: Date.now()
                    }, {
                        sender: 'bot',
                        text: "Where should we send the information on all properties matching your preferences?\n\nPlease leave with us your email address and we'll come back to you within 2 hours.",
                        id: Date.now() + 1
                    }]);
                    return null;
                }

            case CONVERSATION_STATES.EMAIL_REQUEST:
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (emailRegex.test(input)) {
                    dispatch({ type: 'SET_EMAIL', payload: input });
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.COMPLETED });
                    return {
                        sender: 'bot',
                        text: "Great! Keep an eye on your inbox—and don't forget your spam folder just in case!\n\nThank you! 😊"
                    };
                } else {
                    return {
                        sender: 'bot',
                        text: "Please enter a valid email address."
                    };
                }

            case CONVERSATION_STATES.COMPLETED:
                try {
                    // Prepare the final preferences
                    const finalPreferences = {
                        ...state.filters,
                        ...state.preferences
                    };

                    // Call the backend to complete the chat
                    await completeChat(
                        sessionId,
                        finalPreferences,
                        state.userEmail,
                        { messages } // conversation summary
                    );

                    return {
                        sender: 'bot',
                        text: "Thank you for using our service! We'll be in touch soon with your personalized property recommendations."
                    };
                } catch (error) {
                    console.error('Error completing chat:', error);
                    return {
                        sender: 'bot',
                        text: "Thank you for using our service! We'll process your preferences and get back to you soon."
                    };
                }

            default:
                return null;
        }
    };

    const sendMessage = async (message) => {
        setLastActiveMessageId(null);
        
        // Add user message
        const userMessageId = Date.now();
        setMessages(prev => [...prev, {
            sender: 'user',
            text: message,
            id: userMessageId
        }]);

        setIsLoading(true);

        try {
            await simulateTyping();
            const botResponse = await handleUserResponse(message);

            if (botResponse) {
                const newMessageId = Date.now() + 1;
                if (botResponse.options) {
                    setLastActiveMessageId(newMessageId);
                }
                setMessages(prev => [...prev, {
                    ...botResponse,
                    id: newMessageId
                }]);
            }
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    // Initialize chat when component mounts
    useEffect(() => {
        const initializeChat = async () => {
            try {
                setIsLoading(true);
                // Call the backend to initiate chat
                const response = await initiateChat(searchCriteria, list4freeUserId);
                setSessionId(response.session_id);

                // Update the conversation state with the search criteria
                dispatch({ 
                    type: 'UPDATE_FILTERS', 
                    payload: {
                        ...searchCriteria,
                        existingFilters: true
                    }
                });

                // Add the initial popup message
                setMessages([{
                    sender: 'bot',
                    text: response.initial_popup,
                    options: ["Yes, please!", "No, thanks."],
                    id: Date.now()
                }]);

            } catch (error) {
                console.error('Error initializing chat:', error);
                // Handle error appropriately
            } finally {
                setIsLoading(false);
            }
        };

        initializeChat();
    }, [searchCriteria, list4freeUserId]); // Only run when search criteria or user ID changes

    // Handle initial response from popup
    useEffect(() => {
        if (initialResponse) {
            // Add a small delay to ensure the initial message is set first
            const timer = setTimeout(() => {
                sendMessage(initialResponse);
            }, 100);

            return () => clearTimeout(timer); // Cleanup timeout
        }
    }, [initialResponse]); // Only run when initialResponse changes

    // Auto-scroll to bottom when messages change
    useEffect(() => {
        if (chatLogRef.current) {
            chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight;
        }
    }, [messages]);

    // Function to determine if input should be enabled
    const isInputEnabled = () => {
        return state.currentState === CONVERSATION_STATES.BEDROOMS || 
               state.currentState === CONVERSATION_STATES.EMAIL_REQUEST ||
               state.currentState === CONVERSATION_STATES.EDIT_LOCATION;
    };

    // Focus input when entering bedrooms or email state
    useEffect(() => {
        if (isInputEnabled() && inputRef.current) {
            inputRef.current.focus();
        }
    }, [state.currentState]);

    // Clear error when state changes or when input changes
    useEffect(() => {
        setInputError('');
    }, [state.currentState]);

    const handleInputChange = (e) => {
        setUserInput(e.target.value);
        setInputError(''); // Clear error when user types
    };

    const renderMessageContent = (msg) => {
        return (
            <div className={`message-content ${msg.isHint ? 'hint-container' : ''}`}>
                {msg.text && (
                    <div className={msg.isHint ? 'hint-text' : ''}>
                        {msg.text.split('\n').map((line, i) => (
                            <p key={i}>{line}</p>
                        ))}
                    </div>
                )}
                {msg.options && msg.id === lastActiveMessageId && (
                    <div className="options">
                        {msg.options.map((option, i) => (
                            <button
                                key={i}
                                onClick={() => sendMessage(option)}
                                className="option-button"
                                disabled={isLoading}
                            >
                                {option}
                            </button>
                        ))}
                    </div>
                )}
            </div>
        );
    };

    if (isMinimized) {
        return <MinimizedChat onMaximize={() => setIsMinimized(false)} />;
    }

    return (
        <div className="chat-widget">
            <div className="chat-header">
                <div className="header-content">
                    <div className="profile-section">
                        <div className="profile-pic">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z" />
                            </svg>
                        </div>
                        <div className="profile-info">
                            <span>List4Free Assistant 👋</span>
                        </div>
                    </div>
                    <button
                        className="minimize-button"
                        onClick={() => setIsMinimized(true)}
                        aria-label="Minimize chat"
                    >
                        <svg width="12" height="12" viewBox="0 0 12 12" fill="white" xmlns="http://www.w3.org/2000/svg">
                            <path d="M2 6L6 10L10 6" stroke="white" strokeWidth="2" strokeLinecap="round" />
                        </svg>
                    </button>
                </div>
            </div>

            <div className="chat-log" ref={chatLogRef}>
                {messages.map((message, index) => (
                    <div key={message.id || index} className={`message ${message.sender}`}>
                        <div className="message-content">
                            {renderMessageContent(message)}
                        </div>
                    </div>
                ))}
                {isTyping && (
                    <div className="message bot">
                        <TypingIndicator />
                    </div>
                )}
            </div>

            <form onSubmit={(e) => {
                e.preventDefault();
                if (userInput.trim() && !isLoading && isInputEnabled()) {
                    if (state.currentState === CONVERSATION_STATES.EMAIL_REQUEST) {
                        if (validateInput(userInput, 'email')) {
                            setInputError(''); // Clear error
                            sendMessage(userInput);
                            setUserInput('');
                        } else {
                            setInputError('Please enter a valid email address');
                        }
                    } else {
                        sendMessage(userInput);
                        setUserInput('');
                    }
                }
            }}>
                <div className="input-container">
                    {inputError && <div className="input-error">{inputError}</div>}
                    <input
                        ref={inputRef}
                        type="text"
                        value={userInput}
                        onChange={handleInputChange}
                        placeholder={
                            state.currentState === CONVERSATION_STATES.BEDROOMS 
                                ? "Enter number of bedrooms..." 
                                : state.currentState === CONVERSATION_STATES.EMAIL_REQUEST 
                                    ? "Enter your email address..."
                                    : "Type your message..."
                        }
                        disabled={!isInputEnabled()}
                        className={inputError ? 'has-error' : ''}
                    />
                    <button 
                        type="submit" 
                        disabled={!isInputEnabled() || !userInput.trim() || isLoading}
                    >
                        {/* {isLoading ? '...' : 'Send'} */}
                        Send
                    </button>
                </div>
            </form>
        </div>
    );
};

export default ChatWidget;