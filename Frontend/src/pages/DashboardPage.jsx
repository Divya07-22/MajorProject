import React, { useState } from 'react';
import styled from 'styled-components';
import Sidebar from '../components/layout/Sidebar';
import DashboardGrid from '../components/layout/DashboardGrid';
import ScorePanel from '../components/dashboard/ScorePanel';
import TransactionDetails from '../components/dashboard/TransactionDetails';
import ActivityFeed from '../components/dashboard/ActivityFeed';

const MainContent = styled.main`
  padding: ${({ theme }) => theme.spacing.large};
  display: grid;
  gap: ${({ theme }) => theme.spacing.large};
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto 1fr;
  height: 100vh;
  overflow-y: auto;
`;

const DashboardPage = () => {
    const [result, setResult] = useState(null);

    return (
        <DashboardGrid>
            <Sidebar />
            <MainContent>
                <ScorePanel score={result?.risk_score || 0} />
                <TransactionDetails setResult={setResult} />
                <ActivityFeed result={result} />
            </MainContent>
        </DashboardGrid>
    );
};

export default DashboardPage;