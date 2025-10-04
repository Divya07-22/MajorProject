// src/pages/AdminLoginPage.jsx (Updated with Strong Validation)

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { useAuth } from '../hooks/useAuth';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';

const LoginWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
`;
const Title = styled.h2`
  text-align: center;
  margin-bottom: 2rem;
`;
const ErrorMessage = styled.p`
  color: ${({ theme }) => theme.colors.danger};
  text-align: center;
  margin-bottom: 1rem;
`;

const AdminLoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const { login } = useAuth();

    // --- THIS IS THE NEW VALIDATION LOGIC ---
    const validate = () => {
        if (!/\S+@\S+\.\S+/.test(email)) {
            setError('Please enter a valid email format.');
            return false;
        }
        setError('');
        return true;
    };
    // --- END OF NEW LOGIC ---

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // First, validate the input format
        if (!validate()) {
            return;
        }

        // Second, check the credentials
        if (email === "admin@example.com" && password === "AdminPassword123") {
             try {
                // This part is just for the demo to work without a real admin in the DB
                // In a real app, you would have a separate admin login API endpoint
                await login({ email, password: "Password123" }); // Using a dummy password that exists
                navigate('/admin');
            } catch (err) {
                setError('Admin authentication failed on the server.');
            }
        } else {
            setError('Invalid admin credentials.');
        }
    };

    return (
        <LoginWrapper>
            <Card style={{width: '400px'}}>
                <Title>Admin Secure Login</Title>
                <form onSubmit={handleSubmit}>
                    <Input 
                        type="email" 
                        placeholder="Admin Email" 
                        value={email} 
                        onChange={e => setEmail(e.target.value)} 
                        error={error.includes('email')}
                        required 
                    />
                    <Input 
                        type="password" 
                        placeholder="Admin Password" 
                        value={password} 
                        onChange={e => setPassword(e.target.value)} 
                        required 
                    />
                    {error && <ErrorMessage>{error}</ErrorMessage>}
                    <Button type="submit">Login as Admin</Button>
                </form>
            </Card>
        </LoginWrapper>
    );
};

export default AdminLoginPage;