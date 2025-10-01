import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import GlobalStyles from './styles/GlobalStyles';
import AnimatedBackground from './components/shared/AnimatedBackground';
import { useAuth } from './hooks/useAuth';

import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import UserDashboard from './pages/UserDashboard';
import TransactionAnalysis from './pages/TransactionAnalysis';
import AdminDashboard from './pages/AdminDashboard';

const PrivateRoute = ({ children }) => {
    const { user, loading } = useAuth();
    if (loading) return <div>Loading...</div>;
    return user ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <>
      <GlobalStyles />
      <AnimatedBackground />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        {/* Protected Routes */}
        <Route path="/dashboard" element={<PrivateRoute><UserDashboard /></PrivateRoute>} />
        <Route path="/analysis" element={<PrivateRoute><TransactionAnalysis /></PrivateRoute>} />
        <Route path="/admin" element={<PrivateRoute><AdminDashboard /></PrivateRoute>} />
      </Routes>
    </>
  );
}

export default App;