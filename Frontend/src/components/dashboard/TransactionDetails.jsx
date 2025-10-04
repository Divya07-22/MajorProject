// src/components/dashboard/TransactionDetails.jsx

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

        if (!amount || parseFloat(amount) <= 0) {
            setError('Please enter a valid, positive amount.');
            return;
        }
        if (!recipient.startsWith('0x') || recipient.length !== 42) {
            setError('Please enter a valid Ethereum address (starting with 0x).');
            return;
        }

        // --- THIS IS THE FIX ---
        // We now send only the amount, as the new app.py is smart enough
        // to handle the rest.
        const transactionData = {
            amount: parseFloat(amount)
        };
        // --- END OF FIX ---

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