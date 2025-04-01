/**
 * ChatIcon Component
 * 
 * A clickable icon component that represents the chat interface.
 * Used in both the initial popup and minimized chat states.
 * 
 * Features:
 * - Clickable container
 * - SVG chat icon
 * - Notification badge
 * 
 * @param {Object} props - Component props
 * @param {Function} props.onClick - Callback function when the icon is clicked
 */

import React from 'react';
import '../styles/ChatIcon.css';

const ChatIcon = ({ onClick }) => (
  <div 
    className="chat-icon-container" 
    onClick={onClick} 
    role="button" 
    tabIndex={0}
    aria-label="Open chat"
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
    <div className="notification" aria-label="1 new message">1</div>
  </div>
);

export default ChatIcon; 