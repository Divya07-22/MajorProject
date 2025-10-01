import React from 'react';
import styled from 'styled-components';
import Card from '../ui/Card';

const ScoreWrapper = styled(Card)`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

const ScoreLabel = styled.p`
    color: ${({ theme }) => theme.colors.textSecondary};
    font-weight: 500;
`;

const ScoreValue = styled.h1`
    font-size: 5rem;
    font-weight: 700;
    color: ${({ theme, score }) => score > 0.8 ? theme.colors.danger : score > 0.5 ? '#E2B225' : theme.colors.success};
`;

const ScorePanel = ({ score }) => (
    <ScoreWrapper>
        <ScoreLabel>Overall Risk Score</ScoreLabel>
        <ScoreValue score={score}>{Math.round(score * 100)}</ScoreValue>
    </ScoreWrapper>
);

export default ScorePanel;