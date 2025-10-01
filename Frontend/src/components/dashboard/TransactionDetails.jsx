import React from 'react';
import Card from '../ui/Card';
import StatBox from '../ui/StatBox';
import styled from 'styled-components';
import Button from '../ui/Button';
import api from '../../services/api';

const DetailsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: ${({ theme }) => theme.spacing.medium};
`;

const TransactionDetails = ({ setResult }) => {
    const handleTransaction = async () => {
        const mockTransaction = {
            Time: 1727, V1: -1.8, V2: -0.4, V3: 1.5, V4: -0.4, V5: -1.5, V6: -0.8, V7: -0.9,
            V8: 0.3, V9: -1.3, V10: -1.2, V11: 0.1, V12: -1.9, V13: -1.6, V14: -0.5,
            V15: 0.2, V16: -1.8, V17: 0.5, V18: -2.3, V19: 1.1, V20: -0.2, V21: 0.4,
            V22: 0.1, V23: -0.2, V24: 0.0, V25: 0.1, V26: 0.0, V27: 0.3, V28: 0.1,
            Amount: 150.0
        };
        try {
            const response = await api.post('/transaction', mockTransaction);
            setResult(response.data);
        } catch (error) {
            console.error("Transaction failed", error);
            setResult({ error: "Failed to process transaction." });
        }
    };

    return (
        <Card>
            <h3>Initiate Transaction</h3>
            <p style={{color: '#888', margin: '8px 0 16px 0'}}>Click to send a sample high-risk transaction to the backend.</p>
            <Button onClick={handleTransaction}>Process Sample Transaction</Button>
        </Card>
    );
};

export default TransactionDetails;