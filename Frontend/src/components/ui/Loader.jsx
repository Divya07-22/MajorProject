import React from 'react';
import styled, { keyframes } from 'styled-components';

const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const LoaderWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: ${({ theme }) => theme.spacing.medium};
`;

const Spinner = styled.div`
  border: 4px solid ${({ theme }) => theme.colors.secondary};
  border-top: 4px solid ${({ theme }) => theme.colors.primary};
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: ${spin} 1s linear infinite;
`;

const LoaderText = styled.p`
  color: ${({ theme }) => theme.colors.textSecondary};
  font-weight: 600;
`;

const Loader = ({ text }) => (
  <LoaderWrapper>
    <Spinner />
    <LoaderText>{text}</LoaderText>
  </LoaderWrapper>
);

export default Loader;