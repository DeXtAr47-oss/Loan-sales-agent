import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ChatProvider } from './context/ChatContext';
import HomePage from './components/HomePage';
import ChatWindow from './components/ChatWindow';
import Sidebar from './components/Sidebar';

function ChatLayout() {
  return (
    <div className="app-container">
      <Sidebar />
      <main className="main-content">
        <ChatWindow />
      </main>
    </div>
  );
}

function App() {
  return (
    <Router>           {/* ← OUTERMOST */}
      <ChatProvider>   {/* ← Inside Router */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/chat" element={<ChatLayout />} />
        </Routes>
      </ChatProvider>
    </Router>
  );
}

export default App;