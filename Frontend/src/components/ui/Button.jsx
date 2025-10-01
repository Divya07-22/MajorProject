import styled from 'styled-components';

const Button = styled.button`
  width: 100%;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  background: ${({ theme, variant }) => variant === 'secondary' ? 'transparent' : theme.colors.primary};
  color: ${({ theme, variant }) => variant === 'secondary' ? theme.colors.primary : theme.colors.background};
  font-size: ${({ theme }) => theme.fontSizes.medium};
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  box-shadow: ${({ theme, variant }) => variant === 'secondary' ? 'none' : theme.shadows.glow};
  border: ${({ theme, variant }) => variant === 'secondary' ? `2px solid ${theme.colors.primary}` : 'none'};

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 25px ${({ theme }) => theme.colors.glow};
  }
`;

export default Button;