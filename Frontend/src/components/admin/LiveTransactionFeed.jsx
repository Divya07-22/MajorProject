import React from 'react';
import styled from 'styled-components';
import Card from '../ui/Card';

const FeedWrapper = styled(Card)`
  max-width: 100%;
`;

const Title = styled.h3`
  margin-bottom: ${({ theme }) => theme.spacing.medium};
`;

const FeedItem = styled.div`
  padding: 10px;
  border-bottom: 1px solid ${({ theme }) => theme.colors.secondary};
  &:last-child {
    border-bottom: none;
  }
`;

const LiveTransactionFeed = () => (
    <FeedWrapper>
        <Title>Live Transaction Feed</Title>
        <FeedItem>User test@example.com initiated a transaction of 2.1 ETH (HIGH RISK)</FeedItem>
        <FeedItem>User another@example.com initiated a transaction of 0.05 ETH (Low Risk)</FeedItem>
    </FeedWrapper>
);

export default LiveTransactionFeed;