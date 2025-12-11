import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import Card from '../ui/Card';

const ScoreWrapper = styled(Card)`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
`;

const ScoreLabel = styled.p`
    color: ${({ theme }) => theme.colors.textSecondary};
    font-weight: 500;
    margin-bottom: 16px;
`;

const ScoreCircle = styled(motion.div)`
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: conic-gradient(
        ${({ score, theme }) => 
            score > 80 ? theme.colors.danger :
            score > 50 ? theme.colors.warning :
            theme.colors.success
        } ${({ score }) => score * 3.6}deg,
        ${({ theme }) => theme.colors.border} 0deg
    );
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 32px ${({ theme }) => theme.colors.shadow};
`;

const ScoreInner = styled.div`
    width: 85%;
    height: 85%;
    background: ${({ theme }) => theme.colors.panel};
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
`;

const ScoreValue = styled.h1`
    font-size: 3rem;
    font-weight: 700;
    color: ${({ score, theme }) => 
        score > 80 ? theme.colors.danger :
        score > 50 ? theme.colors.warning :
        theme.colors.success
    };
`;

const ScorePanel = ({ score }) => {
    const displayScore = Math.round(score * 100);
    
    return (
        <ScoreWrapper>
            <ScoreLabel>Overall Risk Score</ScoreLabel>
            <ScoreCircle 
                score={displayScore}
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', duration: 0.8 }}
            >
                <ScoreInner>
                    <ScoreValue score={displayScore}>{displayScore}</ScoreValue>
                </ScoreInner>
            </ScoreCircle>
        </ScoreWrapper>
    );
};

export default ScorePanel;
