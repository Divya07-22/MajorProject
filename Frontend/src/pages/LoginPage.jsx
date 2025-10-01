import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { useAuth } from '../hooks/useAuth';
import PageWrapper from '../components/layout/PageWrapper';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';

const Title = styled.h2`
  text-align: center;
  margin-bottom: ${({ theme }) => theme.spacing.large};
`;
const ErrorMessage = styled.p`
  color: ${({ theme }) => theme.colors.danger};
  text-align: center;
`;

const LoginPage = () => {
    const [credentials, setCredentials] = useState({ email: '', password: '' });
    const [error, setError] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleChange = (e) => {
        setCredentials({ ...credentials, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await login(credentials);
            navigate('/dashboard'); // Redirect to dashboard on successful login
        } catch (err) {
            setError('Login failed. Please check your credentials.');
        }
    };

    return (
        <PageWrapper>
            <Card>
                <Title>Secure Login</Title>
                <form onSubmit={handleSubmit}>
                    <Input name="email" type="email" placeholder="Email Address" onChange={handleChange} required />
                    <Input name="password" type="password" placeholder="Password" onChange={handleChange} required />
                    {error && <ErrorMessage>{error}</ErrorMessage>}
                    <Button type="submit">Login</Button>
                </form>
            </Card>
        </PageWrapper>
    );
};

export default LoginPage;