import React, { createContext, useState, useEffect } from 'react';
import api from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // This part can be expanded later to verify token with backend on page load
    const token = localStorage.getItem('access_token');
    if (token) {
      // In a real app, you'd decode the token to get user info
      setUser({ loggedIn: true });
    }
    setLoading(false);
  }, []);

  const register = async (userData) => {
    return api.post('/register', userData);
  };

  const login = async (credentials) => {
    const response = await api.post('/login', credentials);
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      setUser({ loggedIn: true });
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, register, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};