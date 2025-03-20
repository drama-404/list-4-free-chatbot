import logo from './logo.svg';
import './styles/App.css';
import ChatWidget from './components/ChatWidget';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
        <ChatWidget />
      </header>
    </div>
  );
}

export default App;
