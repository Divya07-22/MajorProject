import React from 'react';
import { useLocation } from 'react-router-dom';
import styled from 'styled-components';
import PageWrapper from '../components/layout/PageWrapper';
import Card from '../components/ui/Card';
import RiskScoreGraph from '../components/analysis/RiskScoreGraph';
import VoiceCallPrompt from '../components/analysis/VoiceCallPrompt';
import Loader from '../components/ui/Loader';

const AnalysisContainer = styled(Card)`
  text-align: center;
  max-width: 700px;
`;

const StatusTitle = styled.h2`
  color: ${({ theme, statusColor }) => statusColor || theme.colors.primary};
  margin-bottom: ${({ theme }) => theme.spacing.medium};
`;

const InfoText = styled.p`
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const TransactionAnalysis = () => {
    const location = useLocation();
    const { isLoading, result, error } = location.state || {};

    if (isLoading) {
        return (
            <PageWrapper>
                <Loader text="Analyzing transaction with multi-layered AI..." />
            </PageWrapper>
        );
    }
    
    if (error) {
        return (
             <PageWrapper>
                <AnalysisContainer>
                    <StatusTitle statusColor="#ff1744">Transaction Failed</StatusTitle>
                    <InfoText>{error.error || "An unknown error occurred."}</InfoText>
                </AnalysisContainer>
            </PageWrapper>
        )
    }

    const riskScore = Math.round((result?.risk_score || 0) * 100);
    const isHighRisk = result?.status?.includes('High Risk');

    return (
        <PageWrapper>
            <AnalysisContainer>
                <StatusTitle statusColor={isHighRisk ? '#ff1744' : '#00e676'}>
                    {result?.status || "Analysis Complete"}
                </StatusTitle>
                
                {result?.risk_score !== undefined && <RiskScoreGraph riskScore={riskScore} />}

                {isHighRisk ? (
                     <VoiceCallPrompt />
                ) : (
                    <InfoText>This transaction appears to be safe.</InfoText>
                )}
            </AnalysisContainer>
        </PageWrapper>
    );
};

export default TransactionAnalysis;