// src/pages/AdminDashboardPage.jsx (Updated and Functional)

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
`;

const RiskCell = styled.td`
    font-weight: 600;
    color: ${({ theme, score }) => score > 0.8 ? theme.colors.danger : score > 0.5 ? '#E2B225' : theme.colors.success};
`;


const AdminDashboardPage = () => {
    const [allLogs, setAllLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchAllTransactions = async () => {
            try {
                // --- THIS IS THE FIX: Call the new, specific admin endpoint ---
                const response = await api.get('/admin/all-logs');
                setAllLogs(response.data);
            } catch (err) {
                console.error("Failed to fetch admin data", err);
                setError('Could not fetch data. Are you logged in as an admin?');
            } finally {
                setLoading(false);
            }
        };
        fetchAllTransactions();
    }, []);

    return (
        <MainContent>
            <Title>Admin Panel: All Transactions</Title>
            <Card>
                {loading && <p>Loading all transactions...</p>}
                {error && <p style={{color: 'red'}}>{error}</p>}
                {!loading && !error && (
                     <Table>
                        <thead>
                            <tr>
                                <th>User Email</th>
                                <th>Timestamp</th>
                                <th>Status</th>
                                <th>Risk Score</th>
                                <th>Blockchain Hash</th>
                            </tr>
                        </thead>
                        <tbody>
                            {allLogs.map(log => (
                                <tr key={log.id}>
                                    <td>{log.user_email}</td>
                                    <td>{new Date(log.timestamp).toLocaleString()}</td>
                                    <td>{log.status}</td>
                                    <RiskCell score={log.risk_score}>{Math.round(log.risk_score * 100)}%</RiskCell>
                                    <td>{log.tx_hash ? `${log.tx_hash.substring(0, 10)}...` : 'N/A'}</td>
                                </tr>
                            ))}
                        </tbody>
                    </Table>
                )}
            </Card>
        </MainContent>
    );
};

export default AdminDashboardPage;