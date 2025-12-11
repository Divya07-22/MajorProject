import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import Card from '../components/ui/Card';
import api from '../services/api';
import toast from 'react-hot-toast';

const DashboardContainer = styled.div`
    display: flex;
    min-height: 100vh;
    background: ${({ theme }) => theme.colors.background};
`;

const Sidebar = styled.aside`
    width: 280px;
    background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    padding: 2rem 1rem;
    display: flex;
    flex-direction: column;
    box-shadow: 4px 0 10px rgba(0,0,0,0.1);
`;

const Logo = styled.div`
    text-align: center;
    margin-bottom: 2rem;
    
    .shield-icon {
        font-size: 48px;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: white;
        font-size: 1.5rem;
        margin: 0;
    }
`;

const Nav = styled.nav`
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
`;

const NavButton = styled.button`
    background: ${props => props.active ? 'rgba(255,255,255,0.15)' : 'transparent'};
    border: none;
    color: white;
    padding: 1rem;
    text-align: left;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s;
    
    &:hover {
        background: rgba(255,255,255,0.1);
        transform: translateX(5px);
    }
`;

const LogoutButton = styled.button`
    background: #f56565;
    border: none;
    color: white;
    padding: 1rem;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    margin-top: auto;
    transition: all 0.3s;
    
    &:hover {
        background: #e53e3e;
    }
`;

const MainContent = styled.main`
    flex: 1;
    padding: 2rem;
    overflow-y: auto;
`;

const Header = styled.header`
    margin-bottom: 2rem;
    
    h1 {
        font-size: 2.5rem;
        background: ${({ theme }) => theme.colors.dangerGradient};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    p {
        color: #666;
    }
`;

const TableCard = styled(Card)`
    overflow-x: auto;
    background: ${({ theme }) => theme.colors.panelGlass};
    backdrop-filter: blur(10px);
`;

const Table = styled.table`
    width: 100%;
    border-collapse: collapse;
    min-width: 800px;
    
    th, td {
        padding: 16px;
        text-align: left;
        border-bottom: 1px solid ${({ theme }) => theme.colors.border};
    }
    
    thead {
        background: rgba(102, 126, 234, 0.1);
    }
    
    th {
        font-weight: 600;
        color: ${({ theme }) => theme.colors.text};
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }
    
    tbody tr {
        transition: ${({ theme }) => theme.transition};
        
        &:hover {
            background: rgba(102, 126, 234, 0.05);
        }
    }
    
    td {
        color: ${({ theme }) => theme.colors.text};
    }
`;

const RiskBadge = styled.span`
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
    background: ${props => {
        if (props.score > 0.65) return 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
        if (props.score > 0.30) return 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)';
        return 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)';
    }};
    color: white;
`;

const StatusBadge = styled.span`
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    background: ${props => {
        if (props.status.includes('High Risk')) return '#fee';
        if (props.status.includes('Medium Risk')) return '#ffeaa7';
        return '#e8f5e9';
    }};
    color: ${props => {
        if (props.status.includes('High Risk')) return '#c53030';
        if (props.status.includes('Medium Risk')) return '#d97706';
        return '#2f855a';
    }};
    font-weight: 500;
`;

const BlockchainHash = styled.code`
    background: rgba(0,0,0,0.05);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.85rem;
    color: #667eea;
`;

const LoadingContainer = styled.div`
    text-align: center;
    padding: 3rem;
    color: ${({ theme }) => theme.colors.text};
`;

const ErrorContainer = styled.div`
    background: #fee;
    border: 1px solid #fcc;
    color: #c33;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
`;

const AdminHistoryPage = () => {
    const [allLogs, setAllLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        fetchAllTransactions();
    }, []);

    const fetchAllTransactions = async () => {
        try {
            const response = await api.get('/admin/all-logs');
            setAllLogs(response.data);
            setLoading(false);
        } catch (err) {
            console.error('Failed to fetch admin data', err);
            setError('Could not fetch transaction data. Please check your admin privileges.');
            toast.error('Failed to load transactions');
            setLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        toast.success('Logged out successfully');
        navigate('/admin/login');
    };

    return (
        <DashboardContainer>
            <Sidebar>
                <Logo>
                    <div className="shield-icon">🛡️</div>
                    <h2>Admin Panel</h2>
                </Logo>

                <Nav>
                    <NavButton onClick={() => navigate('/admin/dashboard')}>
                        📊 Dashboard
                    </NavButton>
                    <NavButton active>
                        📜 All Transactions
                    </NavButton>
                    <NavButton onClick={() => navigate('/admin/users')}>
                        👥 User Management
                    </NavButton>
                </Nav>

                <LogoutButton onClick={handleLogout}>
                    🚪 Logout
                </LogoutButton>
            </Sidebar>

            <MainContent>
                <Header>
                    <h1>📜 Transaction History</h1>
                    <p>All user transactions across the platform</p>
                </Header>

                <TableCard
                    as={motion.div}
                    initial={{ y: 50, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                >
                    {loading && (
                        <LoadingContainer>
                            <p>Loading all transactions...</p>
                        </LoadingContainer>
                    )}
                    
                    {error && (
                        <ErrorContainer>
                            <p>{error}</p>
                        </ErrorContainer>
                    )}
                    
                    {!loading && !error && (
                        <Table>
                            <thead>
                                <tr>
                                    <th>User Email</th>
                                    <th>Timestamp</th>
                                    <th>Amount</th>
                                    <th>Risk Score</th>
                                    <th>Status</th>
                                    <th>Blockchain</th>
                                </tr>
                            </thead>
                            <tbody>
                                {allLogs.length === 0 ? (
                                    <tr>
                                        <td colSpan="6" style={{ textAlign: 'center', padding: '2rem' }}>
                                            No transactions found
                                        </td>
                                    </tr>
                                ) : (
                                    allLogs.map(log => (
                                        <motion.tr 
                                            key={log.id}
                                            initial={{ opacity: 0 }}
                                            animate={{ opacity: 1 }}
                                            transition={{ duration: 0.3 }}
                                        >
                                            <td>{log.user_email || 'N/A'}</td>
                                            <td>{new Date(log.timestamp).toLocaleString()}</td>
                                            <td>₹{log.amount?.toLocaleString() || 'N/A'}</td>
                                            <td>
                                                <RiskBadge score={log.risk_score}>
                                                    {Math.round(log.risk_score * 100)}%
                                                </RiskBadge>
                                            </td>
                                            <td>
                                                <StatusBadge status={log.status}>
                                                    {log.status}
                                                </StatusBadge>
                                            </td>
                                            <td>
                                                {log.tx_hash ? (
                                                    <BlockchainHash>
                                                        {log.tx_hash.substring(0, 10)}...
                                                    </BlockchainHash>
                                                ) : 'N/A'}
                                            </td>
                                        </motion.tr>
                                    ))
                                )}
                            </tbody>
                        </Table>
                    )}
                </TableCard>
            </MainContent>
        </DashboardContainer>
    );
};

export default AdminHistoryPage;
