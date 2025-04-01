/**
 * MinimizedChat Component
 * 
 * A minimized version of the chat interface that can be expanded to full size.
 * Appears when the user minimizes the main chat widget.
 * 
 * Features:
 * - Clickable container to restore chat
 * 
 * @param {Object} props - Component props
 * @param {Function} props.onMaximize - Callback function when user clicks to restore chat
 */

import React from 'react';
import '../styles/MinimizedChat.css';

const MinimizedChat = ({ onMaximize }) => (
    <div 
        className="minimized-chat" 
        onClick={onMaximize}
        role="button"
        tabIndex={0}
        aria-label="Restore chat"
    >
        <div className="chat-icon">
            <svg 
                width="24" 
                height="24" 
                viewBox="0 0 24 24" 
                fill="none" 
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
            >
                <path 
                    d="M20 2H4C2.9 2 2 2.9 2 4V22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2Z" 
                    fill="white"
                />
            </svg>
        </div>
    </div>
);

export default MinimizedChat; 