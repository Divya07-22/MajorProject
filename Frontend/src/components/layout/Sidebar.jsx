import React from 'react';
import styled from 'styled-components';
import { FiGrid, FiLogOut, FiActivity } from 'react-icons/fi';
import { useAuth } from '../../hooks/useAuth';

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
`;

const NavItem = styled.div`
  display: flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing.medium};
  padding: 12px;
  border-radius: ${({ theme }) => theme.borderRadius};
  cursor: pointer;
  color: ${({ theme, active }) => active ? theme.colors.textPrimary : theme.colors.textSecondary};
  background-color: ${({ theme, active }) => active ? theme.colors.border : 'transparent'};
  
  &:hover {
    background-color: ${({ theme }) => theme.colors.border};
    color: ${({ theme }) => theme.colors.textPrimary};
  }
`;

const Sidebar = () => {
  const { logout } = useAuth();
  return (
    <SidebarWrapper>
      <div>
        <Logo>FDS</Logo>
        <div style={{marginTop: '48px'}}>
          <NavItem active><FiGrid size={20} /> Dashboard</NavItem>
          <NavItem><FiActivity size={20} /> Activity</NavItem>
        </div>
      </div>
      <NavItem onClick={logout}><FiLogOut size={20} /> Logout</NavItem>
    </SidebarWrapper>
  );
};

export default Sidebar;