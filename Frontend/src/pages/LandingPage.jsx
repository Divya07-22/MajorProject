import React from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiShield, FiUsers, FiUserCheck } from 'react-icons/fi';

const LandingWrapper = styled.div`
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    position: relative;
    overflow: hidden;

    /* Animated background particles */
    &::before {
        content: '';
        position: absolute;
        width: 400px;
        height: 400px;
        background: ${({ theme }) => theme.colors.primary};
        border-radius: 50%;
        filter: blur(100px);
        opacity: 0.3;
        top: -100px;
        left: -100px;
        animation: float 6s ease-in-out infinite;
    }

    &::after {
        content: '';
        position: absolute;
        width: 300px;
        height: 300px;
        background: ${({ theme }) => theme.colors.success};
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.2;
        bottom: -50px;
        right: -50px;
        animation: float 8s ease-in-out infinite reverse;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
`;

const Content = styled.div`
    text-align: center;
    z-index: 1;
    max-width: 800px;
`;

const Logo = styled(motion.div)`
    width: 100px;
    height: 100px;
    background: ${({ theme }) => theme.colors.primaryGradient};
    border-radius: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 2rem;
    box-shadow: 0 10px 40px ${({ theme }) => theme.colors.shadow};
`;

const Title = styled(motion.h1)`
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    background: ${({ theme }) => theme.colors.primaryGradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;

    @media (max-width: 768px) {
        font-size: 2.5rem;
    }
`;

const Subtitle = styled(motion.p)`
    font-size: 1.3rem;
    color: ${({ theme }) => theme.colors.textSecondary};
    margin-bottom: 3rem;
    line-height: 1.6;
`;

const ButtonContainer = styled(motion.div)`
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    flex-wrap: wrap;
`;

const PortalButton = styled(motion.button)`
    padding: 1.2rem 2.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    border-radius: 16px;
    border: 2px solid ${({ theme }) => theme.colors.border};
    background: ${({ variant, theme }) => 
        variant === 'primary' ? theme.colors.primaryGradient : theme.colors.panelGlass};
    backdrop-filter: blur(10px);
    color: ${({ variant }) => variant === 'primary' ? 'white' : 'inherit'};
    display: flex;
    align-items: center;
    gap: 12px;
    transition: ${({ theme }) => theme.transition};
    box-shadow: 0 4px 15px ${({ theme }) => theme.colors.shadow};

    &:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px ${({ theme }) => theme.colors.shadow};
    }
`;

const LandingPage = () => {
    const navigate = useNavigate();

    return (
        <LandingWrapper>
            <Content>
                <Logo
                    initial={{ scale: 0 }}
                    animate={{ scale: 1, rotate: 360 }}
                    transition={{ duration: 0.8, type: 'spring' }}
                >
                    <FiShield size={50} color="white" />
                </Logo>

                <Title
                    initial={{ y: 50, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.3 }}
                >
                    AI-Powered Fraud Detection
                </Title>

                <Subtitle
                    initial={{ y: 30, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.5 }}
                >
                    Real-time transaction monitoring with blockchain-backed security.
                    <br />Your protection, powered by intelligence.
                </Subtitle>

                <ButtonContainer
                    initial={{ y: 30, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.7 }}
                >
                    <PortalButton
                        variant="primary"
                        onClick={() => navigate('/login')}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        <FiUsers size={24} />
                        User Portal
                    </PortalButton>

                    <PortalButton
                        onClick={() => navigate('/admin/login')}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        <FiUserCheck size={24} />
                        Admin Access
                    </PortalButton>
                </ButtonContainer>
            </Content>
        </LandingWrapper>
    );
};

export default LandingPage;
