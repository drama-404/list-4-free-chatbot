import React, { useState } from 'react';
import './styles/App.css';
import ChatWidget from './components/ChatWidget';
import InitialPopup from './components/InitialPopup';

function App() {
  const [showChat, setShowChat] = useState(false);
  const [showPopup, setShowPopup] = useState(true);

  const handlePopupResponse = (accepted) => {
    setShowPopup(false);
    if (accepted) {
      setShowChat(true);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
        {showPopup && <InitialPopup onResponse={handlePopupResponse} />}
        {showChat && <ChatWidget />}
      </header>
    </div>
  );
}

export default App;
