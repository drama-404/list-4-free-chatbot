import React from 'react';
import '../styles/InitialPopup.css';
import ChatIcon from './ChatIcon';

const InitialPopup = ({ onResponse }) => {
  const handleAccept = () => onResponse(true);

  return (
    <div className="popup-overlay">
      <div className="ios-popup">
        <div className="popup-content">
          <div className="popup-message-container">
            <p>Looks like there aren't any properties matching your search. Would you like us to conduct a deeper search on the web?</p>
            <ChatIcon onClick={handleAccept} />
          </div>
          <div className="popup-buttons">
            <button 
              className="popup-button primary"
              onClick={handleAccept}
            >
              Yes, please!
            </button>
            <button 
              className="popup-button secondary"
              onClick={() => onResponse(false)}
            >
              No, thanks
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InitialPopup; 