import styled from 'styled-components';

const Button = styled.button`
  width: 100%;
  padding: 14px 24px;
  background: ${({ theme, variant }) => 
    variant === 'danger' ? theme.colors.dangerGradient : theme.colors.primaryGradient};
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: ${({ theme }) => theme.transition};
  box-shadow: 0 4px 15px ${({ theme }) => theme.colors.shadow};
  position: relative;
  overflow: hidden;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px ${({ theme }) => theme.colors.shadow};
  }

  &:active {
    transform: translateY(0);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  /* Ripple effect */
  &::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.4);
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
  }

  &:active::after {
    width: 300px;
    height: 300px;
  }
`;

export default Button;
