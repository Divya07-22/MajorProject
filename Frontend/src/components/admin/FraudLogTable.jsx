import React from 'react';
import styled from 'styled-components';
import Card from '../ui/Card';

const TableWrapper = styled(Card)`
  margin-top: ${({ theme }) => theme.spacing.large};
  max-width: 100%;
`;

const Title = styled.h3`
  margin-bottom: ${({ theme }) => theme.spacing.medium};
`;

const FraudLogTable = () => (
    <TableWrapper>
        <Title>Blockchain Fraud Logs</Title>
        <p>Blockchain log data would be displayed here.</p>
    </TableWrapper>
);

export default FraudLogTable;