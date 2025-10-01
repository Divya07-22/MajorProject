import React from 'react';
import styled, { keyframes } from 'styled-components';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import PageWrapper from '../components/layout/PageWrapper';
import Button from '../components/ui/Button';

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const LandingContainer = styled.div`
  text-align: center;
  animation: ${fadeIn} 1.5s ease-in-out;
`;

const Title = styled.h1`
  font-size: 3.5rem;
  font-weight: 700;
  text-shadow: 0 0 15px ${({ theme }) => theme.colors.glow};
  margin-bottom: ${({ theme }) => theme.spacing.medium};
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  color: ${({ theme }) => theme.colors.textSecondary};
  max-width: 600px;
  margin: 0 auto ${({ theme }) => theme.spacing.large};
`;

const ButtonContainer = styled.div`
  display: flex;
  gap: ${({ theme }) => theme.spacing.medium};
  justify-content: center;
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
`;

const LandingPage = () => {
  const navigate = useNavigate(); // Initialize the navigate function

  const handleUserLogin = () => {
    navigate('/login'); // Go to the login page
  };

  const handleAdminLogin = () => {
    navigate('/admin'); // Go to the admin page
  };

  return (
    <PageWrapper>
      <LandingContainer>
        <Title>Aegis: AI Fraud Guardian</Title>
        <Subtitle>
          Experience the future of financial security. Real-time AI analysis,
          blockchain immutability, and instant voice verification.
        </Subtitle>
        <ButtonContainer>
          {/* Add the onClick handlers to the buttons */}
          <Button onClick={handleUserLogin}>Personal Portal</Button>
          <Button onClick={handleAdminLogin} variant="secondary">Admin Console</Button>
        </ButtonContainer>
      </LandingContainer>
    </PageWrapper>
  );
};

export default LandingPage;