import React, { useState } from 'react';
import Card from '../ui/Card';
import styled from 'styled-components';
import Button from '../ui/Button';
import Input from '../ui/Input';
import api from '../../services/api';

const ErrorMessage = styled.p`
  color: ${({ theme }) => theme.colors.danger};
  font-size: 0.9rem;
  margin-top: -10px;
  margin-bottom: 10px;
`;

const TransactionDetails = ({ setResult }) => {
    const [amount, setAmount] = useState('');
    const [recipient, setRecipient] = useState('');
    const [error, setError] = useState('');

    const handleTransaction = async (e) => {
        e.preventDefault();
        setError('');

        // --- Strong Validation ---
        if (!amount || parseFloat(amount) <= 0) {
            setError('Please enter a valid, positive amount.');
            return;
        }
        if (!recipient.startsWith('0x') || recipient.length !== 42) {
            setError('Please enter a valid Ethereum address (starting with 0x).');
            return;
        }
        // --- End of Validation ---

        const transactionData = {
            Time: 1727, V1: -1.8, V2: -0.4, V3: 1.5, V4: -0.4, V5: -1.5, V6: -0.8, V7: -0.9,
            V8: 0.3, V9: -1.3, V10: -1.2, V11: 0.1, V12: -1.9, V13: -1.6, V14: -0.5,
            V15: 0.2, V16: -1.8, V17: 0.5, V18: -2.3, V19: 1.1, V20: -0.2, V21: 0.4,
            V22: 0.1, V23: -0.2, V24: 0.0, V25: 0.1, V26: 0.0, V27: 0.3, V28: 0.1,
            Amount: parseFloat(amount)
        };

        try {
            setResult({ isLoading: true });
            const response = await api.post('/transaction', transactionData);
            setResult(response.data);
        } catch (err) {
            console.error("Transaction failed", err);
            setResult({ error: err.response?.data?.error || "Failed to process transaction." });
        }
    };

    return (
        <Card>
            <h3>Initiate New Transaction</h3>
            <form onSubmit={handleTransaction} style={{marginTop: '16px'}}>
                <Input 
                    placeholder="Recipient's Ethereum Address" 
                    value={recipient} 
                    onChange={e => setRecipient(e.target.value)}
                    error={error.includes('Address')}
                />
                <Input 
                    type="number" 
                    placeholder="Amount" 
                    value={amount} 
                    onChange={e => setAmount(e.target.value)}
                    error={error.includes('amount')}
                />
                {error && <ErrorMessage>{error}</ErrorMessage>}
                <Button type="submit">Process Transaction</Button>
            </form>
        </Card>
    );
};

export default TransactionDetails;