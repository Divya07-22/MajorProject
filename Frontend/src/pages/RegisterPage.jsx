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

const RegisterPage = () => {
    const [formData, setFormData] = useState({ email: '', phone_number: '', address: '', password: '' });
    const [error, setError] = useState('');
    const { register } = useAuth();
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await register(formData);
            navigate('/login'); // Redirect to login after successful registration
        } catch (err) {
            setError('Registration failed. Please try again.');
        }
    };

    return (
        <PageWrapper>
            <Card>
                <Title>Create Your Secure Account</Title>
                <form onSubmit={handleSubmit}>
                    <Input name="email" type="email" placeholder="Email Address" onChange={handleChange} required />
                    <Input name="phone_number" type="text" placeholder="Phone Number (e.g., +91...)" onChange={handleChange} required />
                    <Input name="address" type="text" placeholder="Your Ethereum Address (0x...)" onChange={handleChange} required />
                    <Input name="password" type="password" placeholder="Password" onChange={handleChange} required />
                    {error && <ErrorMessage>{error}</ErrorMessage>}
                    <Button type="submit">Register</Button>
                </form>
            </Card>
        </PageWrapper>
    );
};

export default RegisterPage;