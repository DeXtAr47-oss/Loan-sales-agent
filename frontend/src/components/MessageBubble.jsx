import React from 'react';
import { format } from 'date-fns';
import { User, Bot, Check, CheckCheck } from 'lucide-react';

export default function MessageBubble({ message }) {
  const isBot = message.sender === 'bot';
  const statusIcon = message.status === 'sent' ? <CheckCheck size={14} /> : <Check size={14} />;

  return (
    <div className={`message-wrapper ${isBot ? 'bot' : 'user'}`}>
      <div className="message-avatar">
        {isBot ? <Bot size={18} /> : <User size={18} />}
      </div>
      <div className="message-content">
        <div className={`message-bubble ${isBot ? 'bot' : 'user'}`}>
          <p>{message.text}</p>
        </div>
        <div className="message-meta">
          <span className="timestamp">
            {format(new Date(message.timestamp), 'HH:mm')}
          </span>
          {!isBot && <span className="status-icon">{statusIcon}</span>}
        </div>
      </div>
    </div>
  );
}