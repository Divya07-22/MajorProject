import React, { useState } from 'react';
import styled from 'styled-components';
import Card from '../ui/Card';
import Input from '../ui/Input';
import Button from '../ui/Button';

const FormWrapper = styled(Card)`
  max-width: 600px;
`;
const Title = styled.h3`
  margin-bottom: ${({ theme }) => theme.spacing.medium};
  text-align: center;
`;

const TransactionForm = ({ onSubmit }) => {
    const [recipient, setRecipient] = useState('');
    const [amount, setAmount] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        // Here we would add the other V1-V28 features for a real transaction.
        // For this demo, the backend will use a sample, but we send the core data.
        const mockFullTransaction = {
            Time: 1727,
            V1: -1.8, V2: -0.4, V3: 1.5, V4: -0.4, V5: -1.5, V6: -0.8, V7: -0.9,
            V8: 0.3, V9: -1.3, V10: -1.2, V11: 0.1, V12: -1.9, V13: -1.6, V14: -0.5,
            V15: 0.2, V16: -1.8, V17: 0.5, V18: -2.3, V19: 1.1, V20: -0.2, V21: 0.4,
            V22: 0.1, V23: -0.2, V24: 0.0, V25: 0.1, V26: 0.0, V27: 0.3, V28: 0.1,
            Amount: parseFloat(amount) || 150.0 // Use real amount or default
        };
        onSubmit(mockFullTransaction);
    };

    return (
        <FormWrapper>
            <Title>Initiate a New Transaction</Title>
            <form onSubmit={handleSubmit}>
                <Input placeholder="Recipient's Address (0x...)" value={recipient} onChange={e => setRecipient(e.target.value)} required />
                <Input type="number" placeholder="Amount" value={amount} onChange={e => setAmount(e.target.value)} required />
                <Button type="submit">Analyze & Send</Button>
            </form>
        </FormWrapper>
    );
};

export default TransactionForm;