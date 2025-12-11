import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import { useAuth } from '../hooks/useAuth';
import toast from 'react-hot-toast';
import { validateEmail } from '../utils/validation';

const LoginWrapper = styled.div`
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
`;

const FormCard = styled(Card)`
    width: 100%;
    max-width: 450px;
`;

const Title = styled.h2`
    text-align: center;
    margin-bottom: ${({ theme }) => theme.spacing.large};
    font-size: 2rem;
    background: ${({ theme }) => theme.colors.primaryGradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
`;

const ErrorMessage = styled(motion.p)`
    color: ${({ theme }) => theme.colors.danger};
    text-align: center;
    margin-bottom: 1rem;
    font-size: 0.95rem;
`;

const Subtext = styled.p`
    text-align: center;
    margin-top: 1rem;
    color: ${({ theme }) => theme.colors.textSecondary};
`;

const StyledLink = styled(Link)`
    color: ${({ theme }) => theme.colors.primary};
    text-decoration: none;
    font-weight: 600;
    &:hover {
        text-decoration: underline;
    }
`;

const LoginPage = () => {
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
            setError('Please enter a valid email address');
            return;
        }

        if (!password) {
            setError('Password is required');
            return;
        }

        setLoading(true);
        try {
            await login({ email, password });
            toast.success('Login successful!');
            navigate('/dashboard');
        } catch (error) {
            setError('Invalid credentials. Please try again.');
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
                transition={{ duration: 0.5 }}
            >
                <Title>Welcome Back</Title>
                <form onSubmit={handleSubmit}>
                    <Input 
                        type="email" 
                        placeholder="Email Address" 
                        value={email} 
                        onChange={e => setEmail(e.target.value)} 
                        required 
                    />
                    <Input 
                        type="password" 
                        placeholder="Password" 
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
                    <Button type="submit" disabled={loading}>
                        {loading ? <LoadingSpinner size="24px" /> : 'Login'}
                    </Button>
                </form>
                <Subtext>
                    Don't have an account? <StyledLink to="/register">Register here</StyledLink>
                </Subtext>
            </FormCard>
        </LoginWrapper>
    );
};

export default LoginPage;
