import React from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import PageWrapper from '../components/layout/PageWrapper';
import Header from '../components/layout/Header';
import TransactionForm from '../components/dashboard/TransactionForm';
import TransactionHistory from '../components/dashboard/TransactionHistory';

const DashboardContainer = styled.div`
  padding-top: 100px;
  width: 100%;
  max-width: 900px;
`;
const WelcomeMessage = styled.h2`
  margin-bottom: ${({ theme }) => theme.spacing.large};
  text-align: center;
`;

const UserDashboard = () => {
    const navigate = useNavigate();

    const handleTransactionSubmit = async (transactionData) => {
        try {
            // Navigate to analysis page immediately to show loading state
            navigate('/analysis', { state: { isLoading: true } });
            
            const response = await api.post('/transaction', transactionData);
            
            // Navigate again to analysis page, this time with the real response data
            navigate('/analysis', { state: { isLoading: false, result: response.data } });

        } catch (error) {
            console.error("Transaction failed", error);
            // Navigate to analysis page with an error message
            const errorData = error.response ? error.response.data : { error: "Network Error" };
            navigate('/analysis', { state: { isLoading: false, error: errorData } });
        }
    };

    return (
        <>
            <Header />
            <PageWrapper>
                <DashboardContainer>
                    <WelcomeMessage>Welcome, User!</WelcomeMessage>
                    <TransactionForm onSubmit={handleTransactionSubmit} />
                    <TransactionHistory />
                </DashboardContainer>
            </PageWrapper>
        </>
    );
};

export default UserDashboard;