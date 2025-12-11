import React from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import GlobalStyles from './styles/GlobalStyles';
import { useAuth } from './hooks/useAuth';
import Sidebar from './components/layout/Sidebar';
import DashboardGrid from './components/layout/DashboardGrid';
import Toast from './components/ui/Toast';

// User Pages
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import HistoryPage from './pages/HistoryPage';

// Admin Pages
import AdminLoginPage from './pages/AdminLoginPage';
import AdminDashboardPage from './pages/AdminDashboardPage';
import AdminHistoryPage from './pages/AdminHistoryPage';
import AdminUsersPage from './pages/AdminUsersPage';

const PrivateRoute = ({ children }) => {
    const { user } = useAuth();
    return user ? children : <Navigate to="/login" />;
};

const AdminPrivateRoute = ({ children }) => {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const token = localStorage.getItem('token');
    
    if (!token || user.role !== 'admin') {
        return <Navigate to="/admin/login" />;
    }
    
    return children;
};

const UserLayout = ({ children, theme, toggleTheme }) => (
    <DashboardGrid>
        <Sidebar theme={theme} toggleTheme={toggleTheme} />
        {children}
    </DashboardGrid>
);

function App({ theme, toggleTheme }) {
  const location = useLocation();

  return (
    <>
      <GlobalStyles />
      <Toast />
      
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        {/* Admin login (public) */}
        <Route path="/admin/login" element={<AdminLoginPage />} />
        
        {/* Admin routes (protected, no sidebar - built into pages) */}
        <Route path="/admin/dashboard" element={<AdminPrivateRoute><AdminDashboardPage /></AdminPrivateRoute>} />
        <Route path="/admin/history" element={<AdminPrivateRoute><AdminHistoryPage /></AdminPrivateRoute>} />
        <Route path="/admin/users" element={<AdminPrivateRoute><AdminUsersPage /></AdminPrivateRoute>} />
        <Route path="/admin" element={<Navigate to="/admin/dashboard" />} />
        
        {/* User routes (protected, with sidebar) */}
        <Route 
          path="/dashboard" 
          element={
            <PrivateRoute>
              <UserLayout theme={theme} toggleTheme={toggleTheme}>
                <DashboardPage />
              </UserLayout>
            </PrivateRoute>
          } 
        />
        <Route 
          path="/history" 
          element={
            <PrivateRoute>
              <UserLayout theme={theme} toggleTheme={toggleTheme}>
                <HistoryPage />
              </UserLayout>
            </PrivateRoute>
          } 
        />
        
        {/* Catch all */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </>
  );
}

export default App;
