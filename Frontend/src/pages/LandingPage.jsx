// src/pages/LandingPage.jsx

import React from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';

const LandingWrapper = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    text-align: center;
`;

const Title = styled.h1`
    font-size: 4rem;
    font-weight: 700;
    margin-bottom: 1rem;
`;

const Subtitle = styled.p`
    font-size: 1.2rem;
    color: ${({ theme }) => theme.colors.textSecondary};
    margin-bottom: 3rem;
`;

const ButtonContainer = styled.div`
    display: flex;
    gap: 1.5rem;
`;

const PortalButton = styled.button`
    padding: 1rem 2rem;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    border-radius: ${({ theme }) => theme.borderRadius};
    border: 1px solid ${({ theme }) => theme.colors.primary};
    background-color: transparent;
    color: ${({ theme }) => theme.colors.primary};
    transition: all 0.2s;

    &:hover {
        background-color: ${({ theme }) => theme.colors.primary};
        color: white;
    }
`;

const LandingPage = () => {
    const navigate = useNavigate();

    return (
        <LandingWrapper>
            <Title>AI-Powered Fraud Detection System</Title>
            <Subtitle>Your security, reinforced by intelligence.</Subtitle>
            <ButtonContainer>
                <PortalButton onClick={() => navigate('/login')}>Login as User</PortalButton>
                <PortalButton onClick={() => navigate('/admin-login')}>Login as Admin</PortalButton>
            </ButtonContainer>
        </LandingWrapper>
    );
};

export default LandingPage;