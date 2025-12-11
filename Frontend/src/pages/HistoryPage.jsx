import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import Card from '../components/ui/Card';
import api from '../services/api';

const MainContent = styled.main`
  padding: 2rem;
  min-height: 100vh;
  overflow-y: auto;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  margin-bottom: 2rem;
  background: ${({ theme }) => theme.colors.primaryGradient};
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
`;

const Table = styled.table`
    width: 100%;
    border-collapse: collapse;
    
    th, td {
        padding: 14px;
        text-align: left;
    }
    
    thead {
        background: ${({ theme }) => theme.colors.border};
    }
    
    tbody tr {
        border-bottom: 1px solid ${({ theme }) => theme.colors.border};
        transition: ${({ theme }) => theme.transition};

        &:hover {
            background: ${({ theme }) => theme.colors.panelGlass};
        }
    }
`;

const RiskBadge = styled.span`
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    background: ${({ score, theme }) => 
        score > 80 ? theme.colors.dangerGradient :
        score > 50 ? `linear-gradient(135deg, ${theme.colors.warning}, #f6ad55)` :
        theme.colors.successGradient
    };
    color: white;
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
                console.error('Failed to fetch history', error);
            } finally {
                setLoading(false);
            }
        };
        fetchHistory();
    }, []);

    return (
        <MainContent>
            <Title>Transaction History</Title>
            <Card
                as={motion.div}
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
            >
                {loading ? (
                    <p>Loading...</p>
                ) : (
                    <Table>
                        <thead>
                            <tr>
                                <th>Timestamp</th>
                                <th>Amount</th>
                                <th>Risk Score</th>
                                <th>Status</th>
                                <th>Blockchain</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.map(log => (
                                <tr key={log.id}>
                                    <td>{new Date(log.timestamp).toLocaleString()}</td>
                                    <td>₹{log.amount?.toLocaleString() || 'N/A'}</td>
                                    <td>
                                        <RiskBadge score={Math.round(log.risk_score * 100)}>
                                            {Math.round(log.risk_score * 100)}%
                                        </RiskBadge>
                                    </td>
                                    <td>{log.status}</td>
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

export default HistoryPage;
