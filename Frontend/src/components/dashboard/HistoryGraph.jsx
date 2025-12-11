import React from 'react';
import styled from 'styled-components';
import Card from '../ui/Card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const GraphCard = styled(Card)`
    grid-column: 1 / -1;
`;

const HistoryGraph = ({ history }) => {
    const chartData = history.slice(-10).reverse().map((log, idx) => ({
        name: `T${idx + 1}`,
        risk: Math.round(log.risk_score * 100),
    }));

    return (
        <GraphCard>
            <h3>Risk Score Trend</h3>
            <ResponsiveContainer width="100%" height={200}>
                <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#2c2c2c" />
                    <XAxis dataKey="name" stroke="#888" />
                    <YAxis stroke="#888" />
                    <Tooltip 
                        contentStyle={{ 
                            background: 'rgba(30, 30, 46, 0.95)', 
                            border: '1px solid #8b5cf6' 
                        }} 
                    />
                    <Line type="monotone" dataKey="risk" stroke="#8b5cf6" strokeWidth={2} />
                </LineChart>
            </ResponsiveContainer>
        </GraphCard>
    );
};

export default HistoryGraph;
