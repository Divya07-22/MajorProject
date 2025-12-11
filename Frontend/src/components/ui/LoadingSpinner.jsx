import styled, { keyframes } from 'styled-components';

const spin = keyframes`
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
`;

const LoadingSpinner = styled.div`
    width: ${({ size }) => size || '40px'};
    height: ${({ size }) => size || '40px'};
    border: 4px solid ${({ theme }) => theme.colors.border};
    border-top: 4px solid ${({ theme }) => theme.colors.primary};
    border-radius: 50%;
    animation: ${spin} 1s linear infinite;
    margin: 0 auto;
`;

export default LoadingSpinner;
