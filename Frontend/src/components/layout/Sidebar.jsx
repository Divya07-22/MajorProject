import React from 'react';
import styled from 'styled-components';
import { FiGrid, FiLogOut, FiActivity, FiShield } from 'react-icons/fi';
import { useAuth } from '../../hooks/useAuth';
import { NavLink, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import ThemeToggle from '../ui/ThemeToggle';

const SidebarWrapper = styled.div`
  background: ${({ theme }) => theme.colors.panel};
  backdrop-filter: blur(20px);
  border-right: 1px solid ${({ theme }) => theme.colors.border};
  padding: ${({ theme }) => theme.spacing.large};
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100vh;
  position: sticky;
  top: 0;
`;

const Logo = styled(motion.div)`
  width: 60px;
  height: 60px;
  background: ${({ theme }) => theme.colors.primaryGradient};
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 2rem;
  cursor: pointer;
  box-shadow: 0 4px 12px ${({ theme }) => theme.colors.shadow};
`;

const NavItem = styled(NavLink)`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing.medium};
  padding: 14px 16px;
  border-radius: 12px;
  cursor: pointer;
  color: ${({ theme }) => theme.colors.textSecondary};
  text-decoration: none;
  transition: ${({ theme }) => theme.transition};
  margin-bottom: 8px;

  &:hover {
    background: ${({ theme }) => theme.colors.panelGlass};
    color: ${({ theme }) => theme.colors.textPrimary};
  }

  &.active {
    background: ${({ theme }) => theme.colors.primaryGradient};
    color: white;
    box-shadow: 0 4px 12px ${({ theme }) => theme.colors.shadow};
  }
`;

const LogoutButton = styled.div`
    display: flex;
    align-items: center;
    gap: ${({ theme }) => theme.spacing.medium};
    padding: 14px 16px;
    border-radius: 12px;
    cursor: pointer;
    color: ${({ theme }) => theme.colors.textSecondary};
    transition: ${({ theme }) => theme.transition};
    
    &:hover {
        background: ${({ theme }) => theme.colors.dangerGradient};
        color: white;
    }
`;

const SidebarFooter = styled.div`
    display: flex;
    flex-direction: column;
    gap: 12px;
`;

const Sidebar = ({ theme, toggleTheme }) => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
      logout();
      navigate('/login');
  }

  return (
    <SidebarWrapper>
      <div>
        <Logo
          onClick={() => navigate('/dashboard')}
          whileHover={{ scale: 1.05, rotate: 5 }}
          whileTap={{ scale: 0.95 }}
        >
          <FiShield size={30} color="white" />
        </Logo>
        <div>
          <NavItem to="/dashboard"><FiGrid size={20} /> Dashboard</NavItem>
          <NavItem to="/history"><FiActivity size={20} /> History</NavItem>
        </div>
      </div>
      <SidebarFooter>
        <ThemeToggle theme={theme} toggleTheme={toggleTheme} />
        <LogoutButton onClick={handleLogout}><FiLogOut size={20} /> Logout</LogoutButton>
      </SidebarFooter>
    </SidebarWrapper>
  );
};

export default Sidebar;
