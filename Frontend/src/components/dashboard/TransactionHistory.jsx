// src/components/dashboard/TransactionHistory.jsx

import React from 'react';
import styled from 'styled-components';
import Card from '../ui/Card';

const HistoryCard = styled(Card)`
    grid-column: 1 / -1; 
    max-height: 400px;
    overflow-y: auto;
`;

const Table = styled.table`
    width: 100%;
    border-collapse: collapse;
    th, td {
        padding: 12px 15px;
        text-align: left;
        white-space: nowrap;
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

const RiskCell = styled.td`
    font-weight: 600;
    color: ${({ theme, score }) => score > 0.8 ? theme.colors.danger : score > 0.5 ? '#E2B225' : theme.colors.success};
`;

// It now receives history as a prop
const TransactionHistory = ({ history }) => {
    return (
        <HistoryCard>
            <h3>Transaction History</h3>
            <div style={{marginTop: '16px'}}>
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
                        {history.length > 0 ? history.map(log => (
                            <tr key={log.id}>
                                <td>{new Date(log.timestamp).toLocaleString()}</td>
                                <td>{log.status}</td>
                                <RiskCell score={log.risk_score}>{Math.round(log.risk_score * 100)}%</RiskCell>
                                <td>{log.tx_hash ? `${log.tx_hash.substring(0, 10)}...` : 'N/A'}</td>
                            </tr>
                        )) : (
                            <tr>
                                <td colSpan="4" style={{textAlign: 'center', color: '#888'}}>No transactions yet.</td>
                            </tr>
                        )}
                    </tbody>
                </Table>
            </div>
        </HistoryCard>
    );
};

export default TransactionHistory;