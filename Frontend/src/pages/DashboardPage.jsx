// src/pages/DashboardPage.jsx

import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import ScorePanel from '../components/dashboard/ScorePanel';
import TransactionDetails from '../components/dashboard/TransactionDetails';
import ActivityFeed from '../components/dashboard/ActivityFeed';
import TransactionHistory from '../components/dashboard/TransactionHistory';
import HistoryGraph from '../components/dashboard/HistoryGraph'; // <-- IMPORT THE NEW GRAPH
import api from '../services/api';

const MainContent = styled.main`
  padding: ${({ theme }) => theme.spacing.large};
  display: grid;
  gap: ${({ theme }) => theme.spacing.large};
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto 1fr;
  height: 100vh;
  overflow-y: auto;
`;

const DashboardPage = () => {
    const [result, setResult] = useState(null);
    const [history, setHistory] = useState([]);
    const [key, setKey] = useState(0); // Used to force re-fetches

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const response = await api.get('/transactions');
                setHistory(response.data);
            } catch (error) {
                console.error("Failed to fetch transaction history", error);
            }
        };
        fetchHistory();
    }, [key]); // Re-fetch history when key changes

    const handleNewTransaction = (newResult) => {
        setResult(newResult);
        setKey(prevKey => prevKey + 1); // Increment key to trigger re-fetch
    };

    return (
        <MainContent>
            <ScorePanel score={result?.risk_score || 0} />
            <TransactionDetails setResult={handleNewTransaction} />
            <ActivityFeed result={result} />
            <HistoryGraph history={history} /> {/* <-- ADD THE GRAPH COMPONENT */}
            <TransactionHistory history={history} setHistory={setHistory} /> {/* Pass down history */}
        </MainContent>
    );
};

export default DashboardPage;