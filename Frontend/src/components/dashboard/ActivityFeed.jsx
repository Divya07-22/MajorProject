import React from 'react';
import styled from 'styled-components';
import Card from '../ui/Card';
import { FiAlertTriangle, FiCheckCircle, FiInfo } from 'react-icons/fi';

const FeedItem = styled.div`
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: ${({ theme }) => theme.colors.panelGlass};
    border-radius: 8px;
    margin-bottom: 12px;
`;

const IconWrapper = styled.div`
    color: ${({ type, theme }) => 
        type === 'danger' ? theme.colors.danger :
        type === 'success' ? theme.colors.success :
        theme.colors.primary
    };
`;

const ActivityFeed = ({ result }) => (
    <Card>
        <h3>System Activity Log</h3>
        {result && result.isLoading ? (
            <FeedItem>
                <IconWrapper type="info"><FiInfo size={20} /></IconWrapper>
                <p>Analyzing transaction...</p>
            </FeedItem>
        ) : result ? (
            <FeedItem>
                <IconWrapper type={result.risk_score > 0.8 ? 'danger' : 'success'}>
                    {result.risk_score > 0.8 ? <FiAlertTriangle size={20} /> : <FiCheckCircle size={20} />}
                </IconWrapper>
                <div>
                    <p><strong>Status:</strong> {result.status}</p>
                    {result.tx_hash && <p style={{fontSize: '0.85rem', marginTop: '4px'}}>Blockchain: {result.tx_hash.substring(0, 20)}...</p>}
                </div>
            </FeedItem>
        ) : (
            <p style={{marginTop: '16px', color: '#888'}}>Waiting for transaction...</p>
        )}
    </Card>
);

export default ActivityFeed;
