// src/components/layout/Sidebar.jsx

import React from 'react';
import styled from 'styled-components';
import { FiGrid, FiLogOut, FiActivity } from 'react-icons/fi';
import { useAuth } from '../../hooks/useAuth';
import { NavLink, useNavigate } from 'react-router-dom';
import ThemeToggle from '../ui/ThemeToggle'; // <-- IMPORT

const SidebarWrapper = styled.div`
  background-color: ${({ theme }) => theme.colors.panel};
  border-right: 1px solid ${({ theme }) => theme.colors.border};
  padding: ${({ theme }) => theme.spacing.large} ${({ theme }) => theme.spacing.medium};
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100vh;
`;

const Logo = styled.h1`
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 1.5rem;
  text-align: center;
  cursor: pointer;
`;

const NavItem = styled(NavLink)`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing.medium};
  padding: 12px;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  color: ${({ theme }) => theme.colors.textSecondary};
  text-decoration: none;
  transition: all 0.2s;

  &:hover {
    background-color: ${({ theme }) => theme.colors.border};
    color: ${({ theme }) => theme.colors.textPrimary};
  }

  &.active {
    background-color: ${({ theme }) => theme.colors.border};
    color: ${({ theme }) => theme.colors.textPrimary};
  }
`;

const LogoutButton = styled.div`
    /* Styles are same as NavItem but it's not a NavLink */
    display: flex;
    align-items: center;
    gap: ${({ theme }) => theme.spacing.medium};
    padding: 12px;
    border-radius: ${({ theme }) => theme.borderRadius};
    cursor: pointer;
    color: ${({ theme }) => theme.colors.textSecondary};
    text-decoration: none;
    transition: all 0.2s;
    
    &:hover {
        background-color: ${({ theme }) => theme.colors.border};
        color: ${({ theme }) => theme.colors.textPrimary};
    }
`;

const SidebarFooter = styled.div`
    display: flex;
    flex-direction: column;
    gap: 8px;
`;

const Sidebar = ({ theme, toggleTheme }) => { // <-- RECEIVE PROPS
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
      logout();
      navigate('/login');
  }

  return (
    <SidebarWrapper>
      <div>
        <Logo onClick={() => navigate('/dashboard')}>FDS</Logo>
        <div style={{marginTop: '48px', display: 'flex', flexDirection: 'column', gap: '8px'}}>
          <NavItem to="/dashboard"><FiGrid size={20} /> Dashboard</NavItem>
          <NavItem to="/history"><FiActivity size={20} /> History</NavItem>
        </div>
      </div>
      <SidebarFooter>
        <ThemeToggle theme={theme} toggleTheme={toggleTheme} /> {/* <-- ADD THE TOGGLE */}
        <LogoutButton onClick={handleLogout}><FiLogOut size={20} /> Logout</LogoutButton>
      </SidebarFooter>
    </SidebarWrapper>
  );
};

export default Sidebar;