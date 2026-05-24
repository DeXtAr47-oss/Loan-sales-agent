import React, { useState } from 'react';
import { useChat } from '../context/ChatContext';
import AccountForm from './AccountForm';
import EditCustomerForm from './EditCustomerForm';
import {
  X,
  Moon,
  Sun,
  UserPlus,
  User,
  ChevronRight,
  Search
} from 'lucide-react';

export default function SettingsPanel() {
  const {
    theme,
    toggleTheme,
    closeSettings
  } = useChat();

  const [showAccountForm, setShowAccountForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);

  return (
    <>
      <div className="settings-overlay" onClick={closeSettings}>
        <div className="settings-panel" onClick={e => e.stopPropagation()}>
          {/* Header */}
          <div className="settings-header">
            <h2>Settings</h2>
            <button onClick={closeSettings} className="close-btn">
              <X size={20} />
            </button>
          </div>

          {/* Account Section */}
          <div className="settings-section">
            <h3>Account</h3>
            <button
              className="settings-item"
              onClick={() => setShowAccountForm(true)}
            >
              <div className="settings-item-left">
                <div className="settings-icon accent">
                  <UserPlus size={18} />
                </div>
                <div className="settings-item-info">
                  <span className="settings-item-title">Create Account</span>
                  <span className="settings-item-desc">Register for loan services</span>
                </div>
              </div>
              <ChevronRight size={18} className="settings-chevron" />
            </button>

            <button
              className="settings-item"
              onClick={() => setShowEditForm(true)}
            >
              <div className="settings-item-left">
                <div className="settings-icon accent">
                  <Search size={18} />
                </div>
                <div className="settings-item-info">
                  <span className="settings-item-title">Edit Customer</span>
                  <span className="settings-item-desc">Find and modify customer details</span>
                </div>
              </div>
              <ChevronRight size={18} className="settings-chevron" />
            </button>
          </div>

          {/* Appearance Section */}
          <div className="settings-section">
            <h3>Appearance</h3>
            <div className="settings-item" onClick={toggleTheme}>
              <div className="settings-item-left">
                <div className="settings-icon">
                  {theme === 'dark' ? <Moon size={18} /> : <Sun size={18} />}
                </div>
                <div className="settings-item-info">
                  <span className="settings-item-title">Theme</span>
                  <span className="settings-item-desc">{theme === 'dark' ? 'Dark mode' : 'Light mode'}</span>
                </div>
              </div>
              <div className={`toggle-switch ${theme === 'light' ? 'active' : ''}`}>
                <div className="toggle-knob"></div>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="settings-footer">
            <p className="version-text">Version 1.0.0 • Build 2026.05.24</p>
          </div>
        </div>
      </div>

      {showAccountForm && (
        <AccountForm onClose={() => setShowAccountForm(false)} mode="create" />
      )}

      {showEditForm && (
        <EditCustomerForm onClose={() => setShowEditForm(false)} />
      )}
    </>
  );
}