import React, { useState } from 'react';
import './styles/App.css';
import ChatWidget from './components/ChatWidget';
import InitialPopup from './components/InitialPopup';

function App() {
  const [showChat, setShowChat] = useState(false);
  const [showPopup, setShowPopup] = useState(true);
  const [initialResponse, setInitialResponse] = useState(null);

  const handlePopupResponse = (accepted) => {
    setShowPopup(false);
    if (accepted) {
      setShowChat(true);
      setInitialResponse("Yes, please!");
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        {showPopup && <InitialPopup onResponse={handlePopupResponse} />}
        {showChat && <ChatWidget initialResponse={initialResponse} />}
      </header>
    </div>
  );
}

export default App;
