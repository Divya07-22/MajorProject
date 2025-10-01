import React from 'react';
import styled from 'styled-components';
import Card from '../ui/Card';

const HistoryWrapper = styled(Card)`
  margin-top: ${({ theme }) => theme.spacing.large};
  max-width: 100%;
`;

const Title = styled.h3`
  margin-bottom: ${({ theme }) => theme.spacing.medium};
`;

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  text-align: left;
`;

const Th = styled.th`
  padding: 12px;
  border-bottom: 1px solid ${({ theme }) => theme.colors.secondary};
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const Td = styled.td`
  padding: 12px;
  border-bottom: 1px solid ${({ theme }) => theme.colors.secondary};
  
  &.high-risk { color: ${({ theme }) => theme.colors.danger}; }
  &.low-risk { color: ${({ theme }) => theme.colors.success}; }
`;

const mockHistory = [
  { id: 1, date: '2025-10-01 11:30', recipient: '0xabc...', amount: 0.5, risk: 'Low', status: 'Completed' },
  { id: 2, date: '2025-09-30 18:45', recipient: '0xdef...', amount: 2.1, risk: 'High', status: 'Blocked' },
  { id: 3, date: '2025-09-29 09:12', recipient: '0xghi...', amount: 0.1, risk: 'Low', status: 'Completed' },
];

const TransactionHistory = () => (
  <HistoryWrapper>
    <Title>Transaction History</Title>
    <Table>
      <thead>
        <tr>
          <Th>Date</Th>
          <Th>Recipient</Th>
          <Th>Amount</Th>
          <Th>Risk</Th>
          <Th>Status</Th>
        </tr>
      </thead>
      <tbody>
        {mockHistory.map(tx => (
          <tr key={tx.id}>
            <Td>{tx.date}</Td>
            <Td>{tx.recipient}</Td>
            <Td>{tx.amount} ETH</Td>
            <Td className={tx.risk === 'High' ? 'high-risk' : 'low-risk'}>{tx.risk}</Td>
            <Td>{tx.status}</Td>
          </tr>
        ))}
      </tbody>
    </Table>
  </HistoryWrapper>
);

export default TransactionHistory;