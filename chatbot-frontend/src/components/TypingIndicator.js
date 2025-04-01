/**
 * TypingIndicator Component
 * 
 * A visual indicator that shows when the chatbot is "typing" a response.
 * Provides visual feedback to users that the system is processing their input.
 * 
 * Features:
 * - Animated dots sequence
 * - Accessible loading state
 * 
 * Implementation:
 * Uses CSS animations to create a sequence of dots that appear to be typing.
 */

import React from 'react';
import '../styles/TypingIndicator.css';

const TypingIndicator = () => (
    <div 
        className="typing-indicator"
        role="status"
        aria-label="Chatbot is typing"
    >
        <span></span>
        <span></span>
        <span></span>
    </div>
);

export default TypingIndicator; 