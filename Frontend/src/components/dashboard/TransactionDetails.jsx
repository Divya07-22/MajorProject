import React, { useState } from 'react';
import Card from '../ui/Card';
import styled from 'styled-components';
import Button from '../ui/Button';
import Input from '../ui/Input';
import api from '../../services/api';
import toast from 'react-hot-toast';
import { validateAmount, validateEthAddress } from '../../utils/validation';

const ErrorMessage = styled.p`
  color: ${({ theme }) => theme.colors.danger};
  font-size: 0.9rem;
  margin-top: -8px;
  margin-bottom: 10px;
`;

const TransactionDetails = ({ setResult }) => {
    const [amount, setAmount] = useState('');
    const [recipient, setRecipient] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleTransaction = async (e) => {
        e.preventDefault();
        setError('');

        if (!validateAmount(amount)) {
            setError('Amount must be between 0 and 10,000,000');
            return;
        }
        if (!validateEthAddress(recipient)) {
            setError('Invalid Ethereum address (0x + 40 hex characters)');
            return;
        }

        setLoading(true);
        try {
            setResult({ isLoading: true });
            const response = await api.post('/transaction', {
                amount: parseFloat(amount)
            });
            setResult(response.data);
            toast.success('Transaction analyzed!');
        } catch (err) {
            console.error('Transaction failed', err);
            setResult({ error: err.response?.data?.error || 'Failed to process transaction.' });
            toast.error('Transaction failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Card>
            <h3>Initiate New Transaction</h3>
            <form onSubmit={handleTransaction} style={{marginTop: '16px'}}>
                <Input 
                    placeholder="Recipient Ethereum Address (0x...)" 
                    value={recipient} 
                    onChange={e => setRecipient(e.target.value)}
                    error={error.includes('address')}
                />
                <Input 
                    type="number" 
                    placeholder="Amount (₹)" 
                    value={amount} 
                    onChange={e => setAmount(e.target.value)}
                    error={error.includes('Amount')}
                />
                {error && <ErrorMessage>{error}</ErrorMessage>}
                <Button type="submit" disabled={loading}>
                    {loading ? 'Processing...' : 'Analyze Transaction'}
                </Button>
            </form>
        </Card>
    );
};

export default TransactionDetails;
