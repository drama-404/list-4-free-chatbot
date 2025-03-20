import React, { useState, useReducer, useEffect, useRef } from 'react';
import TypingIndicator from './TypingIndicator';
import { CONVERSATION_STATES, PROPERTY_TYPES, TIMELINE_OPTIONS, initialState } from '../utils/conversationState';
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

const ChatWidget = () => {
    const [messages, setMessages] = useState([]);
    const [userInput, setUserInput] = useState('');
    const [state, dispatch] = useReducer(conversationReducer, initialState);
    const [isLoading, setIsLoading] = useState(false);
    const [isTyping, setIsTyping] = useState(false);
    const [isMinimized, setIsMinimized] = useState(false);
    const chatLogRef = useRef(null);

    const API_URL = process.env.REACT_APP_API_URL;
    const CHAT_API_URL = process.env.REACT_APP_CHAT_API_URL;

    //   const getInitialMessage = () => ({
    //     sender: 'bot',
    //     text: "Looks like there aren't any properties matching your search. Would you like us to conduct a deeper search on the web?",
    //     options: ["Yes, please!", "No, thanks."]
    //   });

    const simulateTyping = async () => {
        setIsTyping(true);
        // Simulate typing delay between 1-2 seconds
        await new Promise(resolve => setTimeout(resolve, Math.random() * 1000 + 1000));
        setIsTyping(false);
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

    const handleUserResponse = (input) => {
        switch (state.currentState) {
            case CONVERSATION_STATES.INITIAL:
                if (input === "Yes, please!") {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.LOCATION_INPUT });
                    return {
                        sender: 'bot',
                        text: "Great! Let's start with the location. Where are you looking to buy?",
                        // We'll add location input handling later
                    };
                } else if (input === "No, thanks.") {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.COMPLETED });
                    return {
                        sender: 'bot',
                        text: "Thank you for your time. Feel free to come back if you change your mind!"
                    };
                }
                break;

            case CONVERSATION_STATES.LOCATION_INPUT:
                // Store location input
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
                let selectedType = input;
                dispatch({ 
                    type: 'UPDATE_FILTERS', 
                    payload: { propertyType: selectedType } 
                });

                // If residential is selected, ask for bedrooms
                if (selectedType === PROPERTY_TYPES.RESIDENTIAL.label) {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.BEDROOMS });
                    return {
                        sender: 'bot',
                        text: "How many bedrooms are you looking for?",
                        options: ["Studio", "1", "2", "3", "4+", "No preference"]
                    };
                } else {
                    // Skip to public transport for other property types
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.PUBLIC_TRANSPORT });
                    return {
                        sender: 'bot',
                        text: "Do you need public transport close to your property?",
                        options: ["Yes", "No"]
                    };
                }

            case CONVERSATION_STATES.BEDROOMS:
                dispatch({ 
                    type: 'UPDATE_FILTERS', 
                    payload: { bedrooms: { min: input === "4+" ? 4 : parseInt(input) || 0 } } 
                });
                dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.PUBLIC_TRANSPORT });
                return {
                    sender: 'bot',
                    text: "Do you need public transport close to your property?",
                    options: ["Yes", "No"]
                };

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
                    options: TIMELINE_OPTIONS
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
                    return {
                        sender: 'bot',
                        text: "Where should we send the information on all properties matching your preferences?\n\nPlease leave with us your email address and we'll come back to you within 2 hours."
                    };
                }

            case CONVERSATION_STATES.FINANCIAL_READINESS:
                dispatch({ 
                    type: 'UPDATE_PREFERENCES', 
                    payload: { hasPreApprovedLoan: input === "Yes" } 
                });
                
                if (input === "Yes") {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.COMPLETED });
                    return {
                        sender: 'bot',
                        text: "Please note that you may be requested to show a Pre-Approved Loan Agreement before the viewing of a property.\n\nPlease register an account and we shall provide all the available properties that match your requirements.",
                        options: ["Register"]  // You'll need to handle this action separately
                    };
                } else {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.EMAIL_REQUEST });
                    return {
                        sender: 'bot',
                        text: "Where should we send the information on all properties matching your preferences?\n\nPlease leave with us your email address and we'll come back to you within 2 hours."
                    };
                }

            case CONVERSATION_STATES.EMAIL_REQUEST:
                // Basic email validation
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

            default:
                return null;
        }
    };

    const sendMessage = async (input) => {
        setIsLoading(true);
        setMessages(prev => [...prev, { sender: 'user', text: input }]);

        try {
            await simulateTyping();
            const botResponse = handleUserResponse(input);
            
            if (botResponse) {
                setMessages(prev => [...prev, botResponse]);
            } else {
                // API fallback logic here
            }
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                sender: 'bot',
                text: 'Sorry, there was an error processing your request.'
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    // Initialize chat when component mounts
    useEffect(() => {
        setMessages([{
            sender: 'bot',
            text: "Looks like there aren't any properties matching your search. Would you like us to conduct a deeper search on the web?",
            options: ["Yes, please!", "No, thanks."]
        }]);
    }, []);

    // Auto-scroll to bottom when messages change
    useEffect(() => {
        if (chatLogRef.current) {
          chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight;
        }
      }, [messages]);

    const renderMessageContent = (msg) => {
        return (
            <>
                <p>{msg.text}</p>
                {msg.options && (
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
            </>
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
                                <path d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z"/>
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
                            <path d="M2 6L6 10L10 6" stroke="white" strokeWidth="2" strokeLinecap="round"/>
                        </svg>
                    </button>
                </div>
            </div>
            
            <div className="chat-log" ref={chatLogRef}>
                {messages.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.sender}`}>
                        {renderMessageContent(msg)}
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
                if (userInput.trim() && !isLoading) {
                    const inputType = state.currentState === CONVERSATION_STATES.EMAIL_REQUEST ? 'email' : 'text';
                    if (validateInput(userInput, inputType)) {
                        sendMessage(userInput);
                        setUserInput('');
                    } else {
                        setMessages(prev => [...prev, {
                            sender: 'bot',
                            text: `Please enter a valid ${inputType}.`
                        }]);
                    }
                }
            }}>
                <input
                    type="text"
                    value={userInput}
                    onChange={e => setUserInput(e.target.value)}
                    placeholder="Type your message..."
                    disabled={isLoading}
                />
                <button type="submit" disabled={isLoading || !userInput.trim()}>
                    {isLoading ? '...' : 'Send'}
                </button>
            </form>
        </div>
    );
};

export default ChatWidget;