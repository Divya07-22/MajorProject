import React from 'react';
import styled from 'styled-components';
import Button from '../ui/Button';

const HeaderWrapper = styled.header`
  width: 100%;
  padding: ${({ theme }) => theme.spacing.medium} ${({ theme }) => theme.spacing.large};
  background: rgba(10, 10, 26, 0.8);
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  border-bottom: 1px solid ${({ theme }) => theme.colors.secondary};
`;

const Logo = styled.h1`
  font-size: 1.5rem;
  color: ${({ theme }) => theme.colors.primary};
  margin: 0;
  text-shadow: 0 0 5px ${({ theme }) => theme.colors.glow};
`;

const NavLinks = styled.nav`
  display: flex;
  gap: ${({ theme }) => theme.spacing.medium};
`;

const NavLink = styled.a`
  color: ${({ theme }) => theme.colors.textSecondary};
  font-weight: 600;
  cursor: pointer;
  &:hover {
    color: ${({ theme }) => theme.colors.primary};
  }
`;

const Header = () => (
  <HeaderWrapper>
    <Logo>Aegis</Logo>
    <NavLinks>
      <NavLink>Dashboard</NavLink>
      <NavLink>History</NavLink>
      <Button style={{padding: '8px 16px', width: 'auto'}}>Logout</Button>
    </NavLinks>
  </HeaderWrapper>
);

export default Header;