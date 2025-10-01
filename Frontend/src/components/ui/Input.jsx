import styled from 'styled-components';

const Input = styled.input`
  width: 100%;
  padding: 12px;
  margin-bottom: 16px;
  background-color: #121212;
  border: 1px solid ${({ theme, error }) => error ? theme.colors.danger : theme.colors.border};
  border-radius: 8px;
  color: #e0e0e0;
  font-size: 1rem;

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.primary};
  }
`;

export default Input;