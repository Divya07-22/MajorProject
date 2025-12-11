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

const StatsGrid = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
`;

const StatCard = styled(motion.div)`
    background: ${props => {
        if (props.color === 'blue') return 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        if (props.color === 'red') return 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
        if (props.color === 'green') return 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)';
        return 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)';
    }};
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    
    .stat-icon {
        font-size: 3rem;
    }
    
    .stat-info h3 {
        font-size: 2rem;
        margin: 0;
    }
    
    .stat-info p {
        margin: 0;
        opacity: 0.9;
    }
`;

const QuickActions = styled.div`
    margin-top: 2rem;
    
    h2 {
        margin-bottom: 1rem;
        color: ${({ theme }) => theme.colors.text};
    }
`;

const ActionButtons = styled.div`
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
`;

const ActionButton = styled.button`
    background: ${({ theme }) => theme.colors.dangerGradient};
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    transition: transform 0.2s;
    
    &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
`;

const AdminDashboardPage = () => {
    const [stats, setStats] = useState({
        totalTransactions: 0,
        highRiskCount: 0,
        activeUsers: 0,
        todayTransactions: 0
    });
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        fetchStats();
    }, []);

    const fetchStats = async () => {
        try {
            const response = await api.get('/admin/all-logs');
            const transactions = response.data;
            
            const highRisk = transactions.filter(t => t.risk_score > 0.65).length;
            const today = transactions.filter(t => {
                const txDate = new Date(t.timestamp);
                const now = new Date();
                return txDate.toDateString() === now.toDateString();
            }).length;

            const uniqueUsers = new Set(transactions.map(t => t.user_id));

            setStats({
                totalTransactions: transactions.length,
                highRiskCount: highRisk,
                activeUsers: uniqueUsers.size,
                todayTransactions: today
            });
            setLoading(false);
        } catch (error) {
            console.error('Error fetching stats:', error);
            toast.error('Failed to load dashboard stats');
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
                    <NavButton active onClick={() => navigate('/admin/dashboard')}>
                        📊 Dashboard
                    </NavButton>
                    <NavButton onClick={() => navigate('/admin/history')}>
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
                    <h1>🛡️ Admin Control Panel</h1>
                    <p>Real-time Fraud Detection Dashboard</p>
                </Header>

                {loading ? (
                    <p>Loading dashboard statistics...</p>
                ) : (
                    <>
                        <StatsGrid>
                            <StatCard color="blue" initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}>
                                <div className="stat-icon">📊</div>
                                <div className="stat-info">
                                    <h3>{stats.totalTransactions}</h3>
                                    <p>Total Transactions</p>
                                </div>
                            </StatCard>

                            <StatCard color="red" initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ delay: 0.1 }}>
                                <div className="stat-icon">⚠️</div>
                                <div className="stat-info">
                                    <h3>{stats.highRiskCount}</h3>
                                    <p>High-Risk Transactions</p>
                                </div>
                            </StatCard>

                            <StatCard color="green" initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ delay: 0.2 }}>
                                <div className="stat-icon">👥</div>
                                <div className="stat-info">
                                    <h3>{stats.activeUsers}</h3>
                                    <p>Active Users</p>
                                </div>
                            </StatCard>

                            <StatCard color="purple" initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ delay: 0.3 }}>
                                <div className="stat-icon">📅</div>
                                <div className="stat-info">
                                    <h3>{stats.todayTransactions}</h3>
                                    <p>Today's Transactions</p>
                                </div>
                            </StatCard>
                        </StatsGrid>

                        <QuickActions>
                            <h2>Quick Actions</h2>
                            <ActionButtons>
                                <ActionButton onClick={() => navigate('/admin/history')}>
                                    View All Transactions
                                </ActionButton>
                                <ActionButton onClick={() => navigate('/admin/users')}>
                                    Manage Users
                                </ActionButton>
                                <ActionButton onClick={fetchStats}>
                                    Refresh Stats
                                </ActionButton>
                            </ActionButtons>
                        </QuickActions>
                    </>
                )}
            </MainContent>
        </DashboardContainer>
    );
};

export default AdminDashboardPage;
