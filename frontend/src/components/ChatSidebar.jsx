import React, { useRef, useEffect, useState } from 'react';
import { Bot, X, Send, Paperclip, Loader, User } from 'lucide-react';
import { sendMessageToBackend } from '../services/api';

export default function ChatSidebar({ isOpen, onClose, threadId = 'default', prefill = '' }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState(prefill);
  const [file, setFile] = useState(null);
  const [isTyping, setIsTyping] = useState(false);

  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    if (isOpen) {
      textareaRef.current?.focus();
    }
  }, [isOpen]);

  useEffect(() => {
    if (prefill) setInput(prefill);
  }, [prefill]);

  useEffect(() => {
  if (isOpen && messages.length === 0) {
      loadGreeting();
    }
  }, [isOpen]);

  const loadGreeting = async () => {
    setIsTyping(true);

    try {
      const response = await sendMessageToBackend("");

      setMessages([
        {
          id: "welcome",
          text: response.reply,
          sender: "bot"
        }
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleSend = async () => {
    const text = input.trim();
    if (!text && !file) return;

    const userMessage = {
      id: Date.now().toString(),
      text: text || `📎 ${file?.name}`,
      sender: 'user'
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    const attachedFile = file;
    setFile(null);

    try {
      const response = await sendMessageToBackend(text, {
        thread_id: threadId,
        file: attachedFile
      });

      const botMessage = {
        id: Date.now().toString() + '-bot',
        text: response.reply || response.message || response.text ||
          "I'm processing your request. One moment please.",
        sender: 'bot'
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now().toString() + '-err',
        text: "I'm having trouble connecting right now. Please try again in a moment.",
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileChange = (e) => {
    const selected = e.target.files?.[0];
    if (selected) setFile(selected);
  };

  const handleTextareaInput = (e) => {
    setInput(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
  };

  return (
    <>
      {isOpen && <div className="chat-sidebar-overlay" onClick={onClose} />}
      <aside className={`chat-sidebar ${isOpen ? 'open' : ''}`}>
        <header className="chat-sidebar-header">
          <div className="header-left">
            <div className="bot-avatar">
              <Bot size={20} />
            </div>
            <div className="header-info">
              <h2>ABC Finance Assistant</h2>
              <span className="status">
                <span className="status-dot"></span>
                Online
              </span>
            </div>
          </div>
          <button className="icon-btn close-btn" onClick={onClose} title="Close">
            <X size={20} />
          </button>
        </header>

        <div className="messages-container">
          {messages.map((message) => (
            <div key={message.id} className={`message-bubble ${message.sender}`}>
              {message.sender === 'bot' && (
                <div className="bubble-avatar">
                  <Bot size={16} />
                </div>
              )}
              <div className="bubble-content">
                <p>{message.text}</p>
              </div>
              {message.sender === 'user' && (
                <div className="bubble-avatar user-avatar">
                  <User size={16} />
                </div>
              )}
            </div>
          ))}

          {isTyping && (
            <div className="message-bubble bot">
              <div className="bubble-avatar">
                <Bot size={16} />
              </div>
              <div className="bubble-content typing-indicator">
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-area">
          {file && (
            <div className="file-preview">
              <Paperclip size={14} />
              <span>{file.name}</span>
              <button onClick={() => setFile(null)} className="remove-file-btn">
                <X size={14} />
              </button>
            </div>
          )}
          <div className="input-row">
            <button
              className="icon-btn upload-btn"
              onClick={() => fileInputRef.current?.click()}
              title="Attach file"
            >
              <Paperclip size={18} />
            </button>
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
            <textarea
              ref={textareaRef}
              className="chat-textarea"
              value={input}
              onChange={handleTextareaInput}
              onKeyDown={handleKeyDown}
              placeholder="Type your message..."
              rows={1}
            />
            <button
              className="icon-btn send-btn"
              onClick={handleSend}
              disabled={isTyping || (!input.trim() && !file)}
              title="Send"
            >
              {isTyping ? <Loader size={18} className="spinning" /> : <Send size={18} />}
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}
