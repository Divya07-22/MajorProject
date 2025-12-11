import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
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

const UsersGrid = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5rem;
`;

const UserCard = styled(Card)`
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    background: ${({ theme }) => theme.colors.panelGlass};
    backdrop-filter: blur(10px);
    border: 2px solid ${props => props.frozen ? '#f56565' : 'transparent'};
`;

const UserHeader = styled.div`
    display: flex;
    align-items: center;
    gap: 1rem;
    
    .avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: ${({ theme }) => theme.colors.dangerGradient};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: white;
    }
    
    .info {
        flex: 1;
        
        h3 {
            margin: 0 0 0.25rem 0;
            color: ${({ theme }) => theme.colors.text};
        }
        
        p {
            margin: 0;
            color: #666;
            font-size: 0.9rem;
        }
    }
`;

const UserStats = styled.div`
    display: flex;
    gap: 1rem;
    padding: 1rem 0;
    border-top: 1px solid ${({ theme }) => theme.colors.border};
    border-bottom: 1px solid ${({ theme }) => theme.colors.border};
    
    .stat {
        flex: 1;
        text-align: center;
        
        .value {
            font-size: 1.5rem;
            font-weight: 600;
            color: ${({ theme }) => theme.colors.text};
        }
        
        .label {
            font-size: 0.8rem;
            color: #666;
            margin-top: 0.25rem;
        }
    }
`;

const StatusBadge = styled.span`
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    background: ${props => props.frozen ? '#fee' : '#e8f5e9'};
    color: ${props => props.frozen ? '#c53030' : '#2f855a'};
`;

const ActionButton = styled(Button)`
    width: 100%;
    margin-top: 0.5rem;
`;

const LoadingContainer = styled.div`
    text-align: center;
    padding: 3rem;
    color: ${({ theme }) => theme.colors.text};
`;

const AdminUsersPage = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            // Fetch all users
            const logsResponse = await api.get('/admin/all-logs');
            const logs = logsResponse.data;
            
            // Group by user
            const userMap = {};
            logs.forEach(log => {
                if (!userMap[log.user_id]) {
                    userMap[log.user_id] = {
                        id: log.user_id,
                        email: log.user_email,
                        transactions: 0,
                        highRisk: 0,
                        frozen: false
                    };
                }
                userMap[log.user_id].transactions++;
                if (log.risk_score > 0.65) {
                    userMap[log.user_id].highRisk++;
                }
            });
            
            setUsers(Object.values(userMap));
            setLoading(false);
        } catch (error) {
            console.error('Failed to fetch users', error);
            toast.error('Failed to load users');
            setLoading(false);
        }
    };

    const handleFreezeUser = async (userId) => {
        try {
            await api.put('/user/freeze', { user_id: userId });
            toast.success('User account frozen');
            fetchUsers();
        } catch (error) {
            toast.error('Failed to freeze user');
        }
    };

    const handleUnfreezeUser = async (userId) => {
        try {
            await api.put('/user/unfreeze', { user_id: userId });
            toast.success('User account unfrozen');
            fetchUsers();
        } catch (error) {
            toast.error('Failed to unfreeze user');
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
                    <NavButton onClick={() => navigate('/admin/history')}>
                        📜 All Transactions
                    </NavButton>
                    <NavButton active>
                        👥 User Management
                    </NavButton>
                </Nav>

                <LogoutButton onClick={handleLogout}>
                    🚪 Logout
                </LogoutButton>
            </Sidebar>

            <MainContent>
                <Header>
                    <h1>👥 User Management</h1>
                    <p>Manage and monitor user accounts</p>
                </Header>

                {loading ? (
                    <LoadingContainer>
                        <p>Loading users...</p>
                    </LoadingContainer>
                ) : (
                    <UsersGrid>
                        {users.map(user => (
                            <UserCard
                                key={user.id}
                                frozen={user.frozen}
                                as={motion.div}
                                initial={{ scale: 0.9, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                            >
                                <UserHeader>
                                    <div className="avatar">👤</div>
                                    <div className="info">
                                        <h3>{user.email}</h3>
                                        <p>User ID: {user.id}</p>
                                    </div>
                                </UserHeader>

                                <UserStats>
                                    <div className="stat">
                                        <div className="value">{user.transactions}</div>
                                        <div className="label">Transactions</div>
                                    </div>
                                    <div className="stat">
                                        <div className="value">{user.highRisk}</div>
                                        <div className="label">High Risk</div>
                                    </div>
                                </UserStats>

                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <StatusBadge frozen={user.frozen}>
                                        {user.frozen ? '🔒 Frozen' : '✅ Active'}
                                    </StatusBadge>
                                </div>

                                {user.frozen ? (
                                    <ActionButton 
                                        variant="success" 
                                        onClick={() => handleUnfreezeUser(user.id)}
                                    >
                                        🔓 Unfreeze Account
                                    </ActionButton>
                                ) : (
                                    <ActionButton 
                                        variant="danger" 
                                        onClick={() => handleFreezeUser(user.id)}
                                    >
                                        🔒 Freeze Account
                                    </ActionButton>
                                )}
                            </UserCard>
                        ))}
                    </UsersGrid>
                )}
            </MainContent>
        </DashboardContainer>
    );
};

export default AdminUsersPage;
