import React, { createContext, useContext, useReducer, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { sendMessageToBackend } from '../services/api';

const ChatContext = createContext();

const initialState = {
  threadId: null,
  messages: [
    {
      id: uuidv4(),
      text: "Hello! I'm your Loan Sales Assistant. I can help you with loan applications, eligibility checks, interest rates, and repayment options. How can I assist you today?",
      sender: 'bot',
      timestamp: new Date().toISOString(),
      status: 'sent'
    }
  ],
  isTyping: false,
  conversations: [
    { id: '1', title: 'General Inquiry', active: true },
    { id: '2', title: 'Loan Application', active: false },
    { id: '3', title: 'Eligibility Check', active: false }
  ],
  theme: 'dark',
  settingsOpen: false,
};

function chatReducer(state, action) {
  switch (action.type) {
    case 'ADD_MESSAGE':
      return { ...state, messages: [...state.messages, action.payload] };
    case 'SET_TYPING':
      return { ...state, isTyping: action.payload };
    case 'SET_THREAD_ID':
      return { ...state, threadId: action.payload };
    case 'UPDATE_MESSAGE_STATUS':
      return {
        ...state,
        messages: state.messages.map(msg =>
          msg.id === action.payload.id ? { ...msg, status: action.payload.status } : msg
        )
      };
    case 'CLEAR_MESSAGES':
      return { ...state, messages: [initialState.messages[0]] };
    case 'SWITCH_CONVERSATION':
      return {
        ...state,
        conversations: state.conversations.map(conv => ({
          ...conv,
          active: conv.id === action.payload
        }))
      };
    case 'TOGGLE_THEME':
      return { ...state, theme: state.theme === 'dark' ? 'light' : 'dark' };
    case 'TOGGLE_SETTINGS':
      return { ...state, settingsOpen: !state.settingsOpen };
    case 'CLOSE_SETTINGS':
      return { ...state, settingsOpen: false };
    default:
      return state;
  }
}

export function ChatProvider({ children }) {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  const sendMessage = useCallback(async (text) => {
    const userMessage = {
      id: uuidv4(),
      text,
      sender: 'user',
      timestamp: new Date().toISOString(),
      status: 'sending'
    };

    dispatch({ type: 'ADD_MESSAGE', payload: userMessage });
    dispatch({ type: 'UPDATE_MESSAGE_STATUS', payload: { id: userMessage.id, status: 'sent' } });
    dispatch({ type: 'SET_TYPING', payload: true });

    try {
      const response = await sendMessageToBackend(text, {
        thread_id: state.threadId
      });
      const responseThreadId = response.state?.conversation_id;
      if (responseThreadId) {
        dispatch({ type: 'SET_THREAD_ID', payload: responseThreadId });
      }
      const botMessage = {
        id: uuidv4(),
        text: response.message || response.text || "I'm processing your loan request. A representative will contact you shortly.",
        sender: 'bot',
        timestamp: new Date().toISOString(),
        status: 'sent'
      };
      dispatch({ type: 'ADD_MESSAGE', payload: botMessage });
    } catch (error) {
      const errorMessage = {
        id: uuidv4(),
        text: "I apologize, but I'm having trouble connecting to the loan system right now. Please try again or contact support at support@loansales.com",
        sender: 'bot',
        timestamp: new Date().toISOString(),
        status: 'sent'
      };
      dispatch({ type: 'ADD_MESSAGE', payload: errorMessage });
    } finally {
      dispatch({ type: 'SET_TYPING', payload: false });
    }
  }, [state.threadId]);

  const clearChat = useCallback(() => {
    dispatch({ type: 'CLEAR_MESSAGES' });
    dispatch({ type: 'SET_THREAD_ID', payload: null });
  }, []);

  const switchConversation = useCallback((id) => {
    dispatch({ type: 'SWITCH_CONVERSATION', payload: id });
  }, []);

  const toggleTheme = useCallback(() => {
    dispatch({ type: 'TOGGLE_THEME' });
  }, []);

  const toggleSettings = useCallback(() => {
    dispatch({ type: 'TOGGLE_SETTINGS' });
  }, []);

  const closeSettings = useCallback(() => {
    dispatch({ type: 'CLOSE_SETTINGS' });
  }, []);

  return (
    <ChatContext.Provider value={{
      ...state,
      sendMessage,
      clearChat,
      switchConversation,
      toggleTheme,
      toggleSettings,
      closeSettings,
    }}>
      {children}
    </ChatContext.Provider>
  );
}

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) throw new Error('useChat must be used within ChatProvider');
  return context;
};
