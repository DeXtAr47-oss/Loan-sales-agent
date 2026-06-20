import React, { createContext, useContext, useState, useCallback } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      const saved = sessionStorage.getItem('abc_finance_user');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

const login = useCallback((userData) => {
  setUser(userData);

  sessionStorage.setItem(
    "abc_finance_user",
    JSON.stringify(userData)
  );

  sessionStorage.setItem(
    "access_token",
    userData.access_token
  );
}, []);

const logout = useCallback(() => {
  setUser(null);

  sessionStorage.removeItem("abc_finance_user");
  sessionStorage.removeItem("access_token");
}, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, isLoggedIn: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};
