import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import styled from 'styled-components';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { useAuth } from '../hooks/useAuth';

const LoginWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
`;

const Input = styled.input`
  width: 100%;
  padding: 12px;
  margin-bottom: 16px;
  background-color: #121212;
  border: 1px solid #2c2c2c;
  border-radius: 8px;
  color: #e0e0e0;
  font-size: 1rem;
`;

const Title = styled.h2`
  text-align: center;
  margin-bottom: ${({ theme }) => theme.spacing.large};
`;
const ErrorMessage = styled.p`
  color: ${({ theme }) => theme.colors.danger};
  text-align: center;
  margin-bottom: 1rem;
`;
const Subtext = styled.p`
  text-align: center;
  margin-top: 1rem;
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const { login } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await login({ email, password });
            navigate('/dashboard');
        } catch (error) {
            setError('Login Failed. Please check your credentials.');
        }
    };

    return (
        <LoginWrapper>
            <Card style={{width: '400px'}}>
                <Title>Secure Login</Title>
                <form onSubmit={handleSubmit}>
                    <Input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
                    <Input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
                    {error && <ErrorMessage>{error}</ErrorMessage>}
                    <Button type="submit">Login</Button>
                </form>
                <Subtext>Don't have an account? <Link to="/register" style={{color: '#4a90e2'}}>Register here</Link></Subtext>
            </Card>
        </LoginWrapper>
    );
};

export default LoginPage;