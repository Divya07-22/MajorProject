import styled from 'styled-components';

const InputWrapper = styled.div`
  position: relative;
  margin-bottom: ${({ theme }) => theme.spacing.medium};
`;

const StyledInput = styled.input`
  width: 100%;
  padding: 14px 16px;
  background: ${({ theme }) => theme.colors.panelGlass};
  backdrop-filter: blur(10px);
  border: 2px solid ${({ theme, error }) => 
    error ? theme.colors.danger : theme.colors.border};
  border-radius: 12px;
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 1rem;
  transition: ${({ theme }) => theme.transition};

  &:focus {
    outline: none;
    border-color: ${({ theme, error }) => 
      error ? theme.colors.danger : theme.colors.primary};
    box-shadow: 0 0 0 3px ${({ theme, error }) => 
      error ? 'rgba(245, 101, 101, 0.2)' : 'rgba(139, 92, 246, 0.2)'};
  }

  &::placeholder {
    color: ${({ theme }) => theme.colors.textSecondary};
  }
`;

const ValidationIcon = styled.span`
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
`;

const Input = ({ error, valid, ...props }) => (
  <InputWrapper>
    <StyledInput error={error} {...props} />
    {error && <ValidationIcon>❌</ValidationIcon>}
    {valid && <ValidationIcon>✅</ValidationIcon>}
  </InputWrapper>
);

export default Input;
