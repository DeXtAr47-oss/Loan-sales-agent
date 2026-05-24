import React, { useState, useRef } from 'react';
import { useChat } from '../context/ChatContext';
import { Send, Paperclip, Mic } from 'lucide-react';

export default function InputArea() {
  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const { sendMessage, isTyping } = useChat();
  const textareaRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isTyping) return;

    sendMessage(input.trim());
    setInput('');

    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleInput = (e) => {
    setInput(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = e.target.scrollHeight + 'px';
  };

  return (
    <form className="input-area" onSubmit={handleSubmit}>
      <div className="input-container">
        <button type="button" className="attach-btn" title="Attach file">
          <Paperclip size={20} />
        </button>

        <textarea
          ref={textareaRef}
          value={input}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder="Ask about loans, eligibility, rates..."
          rows={1}
          disabled={isTyping}
        />

        {input.trim() ? (
          <button
            type="submit"
            className="send-btn"
            disabled={isTyping || !input.trim()}
          >
            <Send size={20} />
          </button>
        ) : (
          <button
            type="button"
            className={`mic-btn ${isRecording ? 'recording' : ''}`}
            onClick={() => setIsRecording(!isRecording)}
            title="Voice input"
          >
            <Mic size={20} />
          </button>
        )}
      </div>
    </form>
  );
}