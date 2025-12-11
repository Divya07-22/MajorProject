import React from 'react';
import styled from 'styled-components';
import Card from '../ui/Card';

const Table = styled.table`
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
    
    th, td {
        padding: 12px;
        text-align: left;
    }
    thead {
        background: ${({ theme }) => theme.colors.border};
    }
    tbody tr {
        border-bottom: 1px solid ${({ theme }) => theme.colors.border};
    }
`;

const RiskCell = styled.td`
    font-weight: 600;
    color: ${({ theme, score }) => 
        score > 0.8 ? theme.colors.danger : 
        score > 0.5 ? theme.colors.warning : 
        theme.colors.success};
`;

const TransactionHistory = ({ history }) => {
    return (
        <Card>
            <h3>Recent Transactions</h3>
            <Table>
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Amount</th>
                        <th>Risk</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {history.length > 0 ? history.slice(0, 5).map(log => (
                        <tr key={log.id}>
                            <td>{new Date(log.timestamp).toLocaleString()}</td>
                            <td>₹{log.amount?.toLocaleString() || 'N/A'}</td>
                            <RiskCell score={log.risk_score}>{Math.round(log.risk_score * 100)}%</RiskCell>
                            <td>{log.status}</td>
                        </tr>
                    )) : (
                        <tr>
                            <td colSpan="4" style={{textAlign: 'center', color: '#888'}}>No transactions yet</td>
                        </tr>
                    )}
                </tbody>
            </Table>
        </Card>
    );
};

export default TransactionHistory;
