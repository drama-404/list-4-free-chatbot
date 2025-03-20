import React, { useState, useReducer, useEffect } from 'react';
import { CONVERSATION_STATES, initialState } from '../utils/conversationState';
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

    const API_URL = process.env.REACT_APP_API_URL;
    const CHAT_API_URL = process.env.REACT_APP_CHAT_API_URL;

    //   const getInitialMessage = () => ({
    //     sender: 'bot',
    //     text: "Looks like there aren't any properties matching your search. Would you like us to conduct a deeper search on the web?",
    //     options: ["Yes, please!", "No, thanks."]
    //   });

    const handleUserResponse = (input) => {
        switch (state.currentState) {
            case CONVERSATION_STATES.INITIAL:
                if (input === "Yes, please!") {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.CONFIRM_SEARCH });
                    return {
                        sender: 'bot',
                        text: "Just to confirm, you're looking for a property. Do you want to specify your requirements?",
                        options: ["Yes, let's specify", "No, search everything"]
                    };
                } else if (input === "No, thanks.") {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.COMPLETED });
                    return {
                        sender: 'bot',
                        text: "Thank you for your time. Feel free to come back if you change your mind!"
                    };
                }
                break;

            case CONVERSATION_STATES.CONFIRM_SEARCH:
                if (input === "Yes, let's specify") {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.EDIT_FILTERS });
                    return {
                        sender: 'bot',
                        text: "Great! Let's start with the location. Where are you looking to buy?",
                        // We'll add location input handling later
                    };
                } else if (input === "No, search everything") {
                    dispatch({ type: 'UPDATE_STATE', payload: CONVERSATION_STATES.PUBLIC_TRANSPORT });
                    return {
                        sender: 'bot',
                        text: "Do you need public transport close to your property?",
                        options: ["Yes", "No"]
                    };
                }
                break;

            default:
                return null;
        }
    };

    const sendMessage = async (input) => {
        // Add user message to chat
        setMessages(prev => [...prev, { sender: 'user', text: input }]);

        // Get bot response based on conversation state
        const botResponse = handleUserResponse(input);

        if (botResponse) {
            setMessages(prev => [...prev, botResponse]);
        } else {
            try {
                const response = await fetch(`${API_URL}${CHAT_API_URL}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        message: input,
                        conversationState: state.currentState,
                        filters: state.filters,
                        preferences: state.preferences
                    })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                setMessages(prev => [...prev, {
                    sender: 'bot',
                    text: data.message,
                    options: data.options
                }]);
            } catch (error) {
                console.error('Error details:', error);
                setMessages(prev => [...prev, {
                    sender: 'bot',
                    text: 'Sorry, there was an error processing your request.'
                }]);
            }
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

    const handleSend = (e) => {
        e.preventDefault();
        if (userInput.trim()) {
            sendMessage(userInput);
            setUserInput('');
        }
    };

    return (
        <div className="chat-widget">
            <div className="chat-log">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.sender}`}>
                        <p>{msg.text}</p>
                        {msg.options && (
                            <div className="options">
                                {msg.options.map((option, i) => (
                                    <button
                                        key={i}
                                        onClick={() => sendMessage(option)}
                                        className="option-button"
                                    >
                                        {option}
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>
            <form onSubmit={handleSend}>
                <input
                    type="text"
                    value={userInput}
                    onChange={e => setUserInput(e.target.value)}
                    placeholder="Type your message..."
                />
                <button type="submit">Send</button>
            </form>
        </div>
    );
};

export default ChatWidget;