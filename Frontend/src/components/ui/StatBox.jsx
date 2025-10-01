import React from 'react';
import styled from 'styled-components';
import Card from './Card';

const StatWrapper = styled(Card)`
  padding: ${({ theme }) => theme.spacing.medium};
`;
const Label = styled.p`
  color: ${({ theme }) => theme.colors.textSecondary};
  font-size: 0.9rem;
  margin-bottom: 4px;
`;
const Value = styled.p`
  color: ${({ theme }) => theme.colors.textPrimary};
  font-size: 1.5rem;
  font-weight: 600;
`;

const StatBox = ({ label, value }) => (
  <StatWrapper>
    <Label>{label}</Label>
    <Value>{value}</Value>
  </StatWrapper>
);

export default StatBox;