import styled from 'styled-components';

const Card = styled.div`
  background: ${({ theme }) => theme.colors.panel};
  backdrop-filter: blur(20px);
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius};
  padding: ${({ theme }) => theme.spacing.large};
  box-shadow: 0 8px 32px ${({ theme }) => theme.colors.shadow};
  transition: ${({ theme }) => theme.transition};
  animation: fadeIn 0.5s ease-out;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 48px ${({ theme }) => theme.colors.shadow};
  }
`;

export default Card;
