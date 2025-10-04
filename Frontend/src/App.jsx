// src/App.jsx

import React from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import GlobalStyles from './styles/GlobalStyles';
import { useAuth } from './hooks/useAuth';
import Sidebar from './components/layout/Sidebar';
import DashboardGrid from './components/layout/DashboardGrid';

// Import All Pages
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import HistoryPage from './pages/HistoryPage';
import AdminLoginPage from './pages/AdminLoginPage';
import AdminDashboardPage from './pages/AdminDashboardPage';

const PrivateRoute = ({ children }) => {
    const { user } = useAuth();
    return user ? children : <Navigate to="/login" />;
};

// Main layout for pages that have a sidebar
const Layout = ({ children, theme, toggleTheme }) => (
    <DashboardGrid>
        <Sidebar theme={theme} toggleTheme={toggleTheme} />
        {children}
    </DashboardGrid>
);

function App({ theme, toggleTheme }) { // Receive theme props
  const location = useLocation();
  const showSidebar = ['/dashboard', '/history', '/admin'].includes(location.pathname);

  return (
    <>
      <GlobalStyles />
      {showSidebar ? (
        <Layout theme={theme} toggleTheme={toggleTheme}>
            <Routes>
                <Route path="/dashboard" element={<PrivateRoute><DashboardPage /></PrivateRoute>} />
                <Route path="/history" element={<PrivateRoute><HistoryPage /></PrivateRoute>} />
                <Route path="/admin" element={<PrivateRoute><AdminDashboardPage /></PrivateRoute>} />
            </Routes>
        </Layout>
      ) : (
        <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/admin-login" element={<AdminLoginPage />} />
            <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      )}
    </>
  );
}

export default App;