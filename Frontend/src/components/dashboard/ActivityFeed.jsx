import React from 'react';
import Card from '../ui/Card';

const ActivityFeed = ({ result }) => (
    <Card>
        <h3>System Log</h3>
        {result ? (
            <p style={{marginTop: '16px', color: '#e0e0e0'}}>
                Status: {result.status || result.error}
                {result.tx_hash && <><br/>Blockchain Hash: {result.tx_hash}</>}
            </p>
        ) : (
            <p style={{marginTop: '16px', color: '#888'}}>Waiting for a transaction...</p>
        )}
    </Card>
);

export default ActivityFeed;