import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiDollarSign, FiShield, FiActivity } from 'react-icons/fi';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import VoiceCallModal from '../components/ui/VoiceCallModal';
import api from '../services/api';
import toast from 'react-hot-toast';
import { validateAmount, validateEthAddress } from '../utils/validation';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const MainContent = styled.main`
    padding: ${({ theme }) => theme.spacing.large};
    display: grid;
    gap: ${({ theme }) => theme.spacing.large};
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    min-height: 100vh;
    overflow-y: auto;
`;

const StatCard = styled(Card)`
    display: flex;
    align-items: center;
    gap: ${({ theme }) => theme.spacing.medium};
`;

const IconWrapper = styled.div`
    width: 60px;
    height: 60px;
    background: ${({ theme }) => theme.colors.primaryGradient};
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px ${({ theme }) => theme.colors.shadow};
`;

const StatContent = styled.div`
    flex: 1;
`;

const StatLabel = styled.p`
    color: ${({ theme }) => theme.colors.textSecondary};
    font-size: 0.9rem;
    margin-bottom: 4px;
`;

const StatValue = styled.h3`
    font-size: 1.8rem;
    font-weight: 700;
    color: ${({ color }) => color};
`;

const FullWidthCard = styled(Card)`
    grid-column: 1 / -1;
`;

const Title = styled.h3`
    margin-bottom: ${({ theme }) => theme.spacing.medium};
    font-size: 1.3rem;
`;

const RiskGauge = styled.div`
    width: 200px;
    height: 200px;
    margin: 0 auto;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
`;

const RiskCircle = styled(motion.div)`
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: conic-gradient(
        ${({ score, theme }) => 
            score > 80 ? theme.colors.danger :
            score > 50 ? theme.colors.warning :
            theme.colors.success
        } ${({ score }) => score * 3.6}deg,
        ${({ theme }) => theme.colors.border} 0deg
    );
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 32px ${({ theme }) => theme.colors.shadow};
`;

const RiskInner = styled.div`
    width: 85%;
    height: 85%;
    background: ${({ theme }) => theme.colors.panel};
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
`;

const RiskScore = styled.h1`
    font-size: 3rem;
    font-weight: 700;
    color: ${({ score, theme }) => 
        score > 80 ? theme.colors.danger :
        score > 50 ? theme.colors.warning :
        theme.colors.success
    };
`;

const RiskLabel = styled.p`
    color: ${({ theme }) => theme.colors.textSecondary};
    font-size: 0.9rem;
`;

const Table = styled.table`
    width: 100%;
    border-collapse: collapse;
    margin-top: ${({ theme }) => theme.spacing.medium};

    th, td {
        padding: 12px;
        text-align: left;
    }

    thead {
        background: ${({ theme }) => theme.colors.border};
        border-radius: 8px;
    }

    tbody tr {
        border-bottom: 1px solid ${({ theme }) => theme.colors.border};
        transition: ${({ theme }) => theme.transition};

        &:hover {
            background: ${({ theme }) => theme.colors.panelGlass};
        }
    }
`;

const RiskBadge = styled.span`
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    background: ${({ score, theme }) => 
        score > 80 ? theme.colors.dangerGradient :
        score > 50 ? `linear-gradient(135deg, ${theme.colors.warning}, #f6ad55)` :
        theme.colors.successGradient
    };
    color: white;
`;

const DashboardPage = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [formData, setFormData] = useState({ recipient: '', amount: '' });
    const [errors, setErrors] = useState({});
    const [showVoiceCall, setShowVoiceCall] = useState(false);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const response = await api.get('/transactions');
            setHistory(response.data);
        } catch (error) {
            console.error('Failed to fetch history', error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const newErrors = {};
        if (!validateEthAddress(formData.recipient)) {
            newErrors.recipient = 'Invalid Ethereum address';
        }
        if (!validateAmount(formData.amount)) {
            newErrors.amount = 'Amount must be between 0 and 10,000,000';
        }

        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            toast.error('Please fix validation errors');
            return;
        }

        setLoading(true);
        setErrors({});
        try {
            const response = await api.post('/transaction', {
                amount: parseFloat(formData.amount)
            });
            
            setResult(response.data);
            
            // Show voice call modal for high-risk transactions
                        // Show voice call modal for MEDIUM and HIGH-risk transactions
            if (response.data.risk_score >= 0.65) {
                setTimeout(() => setShowVoiceCall(true), 1000);
                toast.error('🚨 HIGH RISK! Transaction blocked!');
            } else if (response.data.risk_score >= 0.30) {
                setTimeout(() => setShowVoiceCall(true), 1000);
                toast('⚠️ MEDIUM RISK! Verification required!', { icon: '⚠️' });
            } else {
                toast.success('✅ Low Risk - Transaction approved!');
            }

            fetchHistory();

        
        } catch (error) {
            toast.error('Transaction failed');
        } finally {
            setLoading(false);
        }
    };

    const handleVoiceCallConfirm = (action) => {
    if (action === 'confirmed') {
        toast.success('✅ Transaction approved by user!');
        setFormData({ recipient: '', amount: '' });
        fetchHistory();  // Refresh transaction list
    } else if (action === 'blocked') {
        toast.error('🚫 Transaction blocked by user!');
        setResult(null);
        setFormData({ recipient: '', amount: '' });
        fetchHistory();  // Refresh transaction list
    } else if (action === 'verify') {
        toast('📧 Verification email sent! Check your inbox.', { 
            icon: '📧',
            duration: 5000 
        });
        // Could call API here: api.post('/verify-transaction', { transaction_id: result.id })
        
        setTimeout(() => fetchHistory(), 500);  // Refresh after 500ms

    }
};


    const avgRiskScore = history.length > 0 
        ? Math.round(history.reduce((acc, h) => acc + h.risk_score, 0) / history.length * 100)
        : 0;

    const chartData = history.slice(-10).reverse().map((log, idx) => ({
        name: `T${idx + 1}`,
        risk: Math.round(log.risk_score * 100),
    }));

    return (
        <MainContent>
            <StatCard
                as={motion.div}
                initial={{ x: -50, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.1 }}
            >
                <IconWrapper>
                    <FiDollarSign size={28} color="white" />
                </IconWrapper>
                <StatContent>
                    <StatLabel>Total Transactions</StatLabel>
                    <StatValue>{history.length}</StatValue>
                </StatContent>
            </StatCard>

            <StatCard
                as={motion.div}
                initial={{ x: -50, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.2 }}
            >
                <IconWrapper>
                    <FiShield size={28} color="white" />
                </IconWrapper>
                <StatContent>
                    <StatLabel>Avg Risk Score</StatLabel>
                    <StatValue color={avgRiskScore >= 65 ? '#f56565' : avgRiskScore >= 30 ? '#ed8936' : '#48bb78'}>

                        {avgRiskScore}%
                    </StatValue>
                </StatContent>
            </StatCard>

            <StatCard
                as={motion.div}
                initial={{ x: -50, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.3 }}
            >
                <IconWrapper>
                    <FiActivity size={28} color="white" />
                </IconWrapper>
                <StatContent>
                    <StatLabel>Flagged Transactions</StatLabel>
                    <StatValue color="#f56565">
                             {history.filter(h => h.risk_score >= 0.65).length} 
                    </StatValue>
                </StatContent>
            </StatCard>

            <FullWidthCard
                as={motion.div}
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4 }}
            >
                <Title>Initiate New Transaction</Title>
                <form onSubmit={handleSubmit}>
                    <Input
                        placeholder="Recipient Ethereum Address (0x...)"
                        value={formData.recipient}
                        onChange={e => setFormData({ ...formData, recipient: e.target.value })}
                        error={errors.recipient}
                    />
                    {errors.recipient && <p style={{color: '#f56565', fontSize: '0.9rem', marginTop: '-8px'}}>{errors.recipient}</p>}
                    
                    <Input
                        type="number"
                        placeholder="Amount (₹)"
                        value={formData.amount}
                        onChange={e => setFormData({ ...formData, amount: e.target.value })}
                        error={errors.amount}
                    />
                    {errors.amount && <p style={{color: '#f56565', fontSize: '0.9rem', marginTop: '-8px'}}>{errors.amount}</p>}
                    
                    <Button type="submit" disabled={loading}>
                        {loading ? <LoadingSpinner size="24px" /> : 'Analyze Transaction'}
                    </Button>
                </form>
            </FullWidthCard>

            {result && (
                <FullWidthCard
                    as={motion.div}
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                >
                    <Title>Risk Analysis Result</Title>
                    <RiskGauge>
                        <RiskCircle score={Math.round(result.risk_score * 100)}>
                            <RiskInner>
                                <RiskScore score={Math.round(result.risk_score * 100)}>
                                    {Math.round(result.risk_score * 100)}
                                </RiskScore>
                                <RiskLabel>Risk Score</RiskLabel>
                            </RiskInner>
                        </RiskCircle>
                    </RiskGauge>
                    <p style={{textAlign: 'center', marginTop: '1rem', fontSize: '1.1rem'}}>
                        {result.status}
                    </p>
                </FullWidthCard>
            )}

            <FullWidthCard
                as={motion.div}
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.5 }}
            >
                <Title>Risk Score Trend</Title>
                <ResponsiveContainer width="100%" height={250}>
                    <AreaChart data={chartData}>
                        <defs>
                            <linearGradient id="riskGradient" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stopColor="#8b5cf6" stopOpacity={0.8}/>
                                <stop offset="100%" stopColor="#8b5cf6" stopOpacity={0.1}/>
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#2c2c2c" />
                        <XAxis dataKey="name" stroke="#888" />
                        <YAxis stroke="#888" />
                        <Tooltip 
                            contentStyle={{ 
                                background: 'rgba(30, 30, 46, 0.95)', 
                                border: '1px solid #8b5cf6',
                                borderRadius: '8px'
                            }} 
                        />
                        <Area type="monotone" dataKey="risk" stroke="#8b5cf6" fill="url(#riskGradient)" />
                    </AreaChart>
                </ResponsiveContainer>
            </FullWidthCard>

            <FullWidthCard
                as={motion.div}
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.6 }}
            >
                <Title>Recent Transactions</Title>
                <Table>
                    <thead>
                        <tr>
                            <th>Timestamp</th>
                            <th>Amount</th>
                            <th>Risk Score</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {history.slice(0, 5).map((log) => (
                            <tr key={log.id}>
                                <td>{new Date(log.timestamp).toLocaleString()}</td>
                                <td>₹{log.amount?.toLocaleString() || 'N/A'}</td>
                                <td>
                                    <RiskBadge score={Math.round(log.risk_score * 100)}>
                                        {Math.round(log.risk_score * 100)}%
                                    </RiskBadge>
                                </td>
                                <td>{log.status}</td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            </FullWidthCard>

            <VoiceCallModal
                isOpen={showVoiceCall}
                onClose={() => setShowVoiceCall(false)}
                transactionAmount={parseFloat(formData.amount)}
                onConfirm={handleVoiceCallConfirm}
            />
        </MainContent>
    );
};

export default DashboardPage;
