// src/components/dashboard/HistoryGraph.jsx

import React from 'react';
import styled from 'styled-components';
import Card from '../ui/Card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const GraphCard = styled(Card)`
    grid-column: 1 / -1; /* Make this component span the full width */
`;

const HistoryGraph = ({ history }) => {
    // Format the data for the chart
    const chartData = history.map(log => ({
        name: new Date(log.timestamp).toLocaleTimeString(),
        risk: Math.round(log.risk_score * 100),
    })).reverse(); // Reverse to show time progression left-to-right

    return (
        <GraphCard>
            <h3>Risk Score Over Time</h3>
            <div style={{ width: '100%', height: 200, marginTop: '1rem' }}>
                <ResponsiveContainer>
                    <LineChart
                        data={chartData}
                        margin={{ top: 5, right: 20, left: -10, bottom: 5 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" stroke="#2c2c2c" />
                        <XAxis dataKey="name" stroke="#888888" />
                        <YAxis stroke="#888888" />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: '#1e1e1e',
                                border: '1px solid #2c2c2c',
                            }}
                        />
                        <Line type="monotone" dataKey="risk" stroke="#4a90e2" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 8 }} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </GraphCard>
    );
};

export default HistoryGraph;