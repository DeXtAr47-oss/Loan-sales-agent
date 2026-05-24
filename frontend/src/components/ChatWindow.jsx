import React, { useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useChat } from '../context/ChatContext';
import MessageBubble from './MessageBubble';
import InputArea from './InputArea';
import TypingIndicator from './TypingIndicator';
import { Bot, ArrowLeft } from 'lucide-react';

export default function ChatWindow() {
  const { messages, isTyping } = useChat();
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  return (
    <div className="chat-window">
      <header className="chat-header">
        <div className="header-left">
          <button
            className="icon-btn back-btn"
            onClick={() => navigate('/')}
            title="Back to Home"
          >
            <ArrowLeft size={20} />
          </button>
          <div className="bot-avatar">
            <Bot size={24} />
          </div>
          <div className="header-info">
            <h2>Loan Sales Agent</h2>
            <span className="status">
              <span className="status-dot"></span>
              Online
            </span>
          </div>
        </div>
        {/* Right side is now empty — settings moved to sidebar */}
      </header>

      <div className="messages-container">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        {isTyping && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      <InputArea />
    </div>
  );
}