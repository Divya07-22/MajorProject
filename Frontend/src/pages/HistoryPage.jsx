// src/pages/HistoryPage.jsx

import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import Sidebar from '../components/layout/Sidebar';
import DashboardGrid from '../components/layout/DashboardGrid';
import Card from '../components/ui/Card';
import api from '../services/api';

const MainContent = styled.main`
  padding: 2rem;
  height: 100vh;
  overflow-y: auto;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  margin-bottom: 2rem;
`;

const Table = styled.table`
    width: 100%;
    border-collapse: collapse;
    th, td {
        padding: 12px 15px;
        text-align: left;
    }
    thead {
        background-color: ${({ theme }) => theme.colors.border};
    }
    tbody tr {
        border-bottom: 1px solid ${({ theme }) => theme.colors.border};
    }
    tbody tr:last-child {
        border-bottom: none;
    }
`;

const HistoryPage = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const response = await api.get('/transactions');
                setHistory(response.data);
            } catch (error) {
                console.error("Failed to fetch transaction history", error);
            } finally {
                setLoading(false);
            }
        };
        fetchHistory();
    }, []);

    return (
        <DashboardGrid>
            <Sidebar />
            <MainContent>
                <Title>Transaction History</Title>
                <Card>
                    {loading ? (
                        <p>Loading history...</p>
                    ) : (
                        <Table>
                            <thead>
                                <tr>
                                    <th>Timestamp</th>
                                    <th>Status</th>
                                    <th>Risk Score</th>
                                    <th>Blockchain Hash</th>
                                </tr>
                            </thead>
                            <tbody>
                                {history.map(log => (
                                    <tr key={log.id}>
                                        <td>{new Date(log.timestamp).toLocaleString()}</td>
                                        <td>{log.status}</td>
                                        <td>{Math.round(log.risk_score * 100)}%</td>
                                        <td>{log.tx_hash ? `${log.tx_hash.substring(0, 10)}...` : 'N/A'}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </Table>
                    )}
                </Card>
            </MainContent>
        </DashboardGrid>
    );
};

export default HistoryPage;