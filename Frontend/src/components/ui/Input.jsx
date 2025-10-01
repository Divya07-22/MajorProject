import styled from 'styled-components';

const Input = styled.input`
  width: 100%;
  padding: 12px;
  margin-bottom: ${({ theme }) => theme.spacing.medium};
  background-color: rgba(10, 10, 26, 0.8);
  border: 1px solid ${({ theme }) => theme.colors.secondary};
  border-radius: 8px;
  color: ${({ theme }) => theme.colors.text};
  font-size: ${({ theme }) => theme.fontSizes.medium};

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.primary};
    box-shadow: 0 0 10px ${({ theme }) => theme.colors.glow};
  }
`;

export default Input;