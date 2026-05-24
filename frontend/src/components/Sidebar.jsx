import React from 'react';
import { useChat } from '../context/ChatContext';
import SettingsPanel from './SettingsPanel';
import { MessageSquare, Plus, Settings, TrendingUp, Calculator, Shield } from 'lucide-react';

export default function Sidebar() {
  const { conversations, switchConversation, settingsOpen, toggleSettings } = useChat();

  const getIcon = (title) => {
    if (title.includes('Application')) return <TrendingUp size={18} />;
    if (title.includes('Eligibility')) return <Calculator size={18} />;
    if (title.includes('General')) return <MessageSquare size={18} />;
    return <Shield size={18} />;
  };

  return (
    <>
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="logo">
            <TrendingUp size={24} />
            <h1>LoanAgent</h1>
          </div>
          <button className="new-chat-btn">
            <Plus size={18} />
            New Chat
          </button>
        </div>

        <nav className="conversations-list">
          {conversations.map((conv) => (
            <button
              key={conv.id}
              className={`conversation-item ${conv.active ? 'active' : ''}`}
              onClick={() => switchConversation(conv.id)}
            >
              {getIcon(conv.title)}
              <span>{conv.title}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <button className="settings-btn" onClick={toggleSettings}>
            <Settings size={18} />
            Settings
          </button>
        </div>
      </aside>

      {settingsOpen && <SettingsPanel />}
    </>
  );
}