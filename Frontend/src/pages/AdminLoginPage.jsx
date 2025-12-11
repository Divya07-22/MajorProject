import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useAuth } from '../hooks/useAuth';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import toast from 'react-hot-toast';
import { validateEmail } from '../utils/validation';

const LoginWrapper = styled.div`
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`;

const FormCard = styled(Card)`
    width: 100%;
    max-width: 450px;
    padding: 3rem;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
`;

const Title = styled.h2`
    text-align: center;
    margin-bottom: ${({ theme }) => theme.spacing.large};
    font-size: 2rem;
    background: ${({ theme }) => theme.colors.dangerGradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
`;

const ShieldIcon = styled.div`
    font-size: 60px;
    text-align: center;
    margin-bottom: 1rem;
`;

const Subtitle = styled.p`
    text-align: center;
    color: #666;
    margin-bottom: 2rem;
    font-size: 0.9rem;
`;

const ErrorMessage = styled(motion.p)`
    color: ${({ theme }) => theme.colors.danger};
    text-align: center;
    margin-bottom: 1rem;
    padding: 12px;
    background: #fee;
    border-radius: 8px;
    border: 1px solid #fcc;
`;

const BackLink = styled.div`
    text-align: center;
    margin-top: 1.5rem;
    
    a {
        color: #667eea;
        text-decoration: none;
        font-size: 0.9rem;
        &:hover {
            text-decoration: underline;
        }
    }
`;

const AdminLoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const { login } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!validateEmail(email)) {
            setError('Please enter a valid email');
            return;
        }

        setLoading(true);
        try {
            const response = await fetch('http://localhost:5000/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            console.log('Login response:', data); // Debug log

            if (!response.ok) {
                setError(data.error || 'Login failed');
                toast.error('Login failed');
                setLoading(false);
                return;
            }

            // Check if user has admin role
            if (!data.user || data.user.role !== 'admin') {
                setError('Access Denied: Admin privileges required');
                toast.error('Not an admin account');
                setLoading(false);
                return;
            }

            // Store credentials
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            // Call useAuth login
            await login({ email, password });
            
            toast.success('Admin login successful!');
            navigate('/admin/dashboard');
        } catch (err) {
            console.error('Login error:', err);
            setError('Admin authentication failed');
            toast.error('Login failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <LoginWrapper>
            <FormCard
                as={motion.div}
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
            >
                <ShieldIcon>🛡️</ShieldIcon>
                <Title>Admin Portal</Title>
                <Subtitle>Access Control Panel</Subtitle>
                
                <form onSubmit={handleSubmit}>
                    <Input 
                        type="email" 
                        placeholder="Admin Email" 
                        value={email} 
                        onChange={e => setEmail(e.target.value)} 
                        required 
                    />
                    <Input 
                        type="password" 
                        placeholder="Admin Password" 
                        value={password} 
                        onChange={e => setPassword(e.target.value)} 
                        required 
                    />
                    {error && (
                        <ErrorMessage
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                        >
                            {error}
                        </ErrorMessage>
                    )}
                    <Button type="submit" variant="danger" disabled={loading}>
                        {loading ? <LoadingSpinner size="24px" /> : 'Secure Login'}
                    </Button>
                </form>
                
                <BackLink>
                    <a href="/login">← Back to User Login</a>
                </BackLink>
            </FormCard>
        </LoginWrapper>
    );
};

export default AdminLoginPage;
