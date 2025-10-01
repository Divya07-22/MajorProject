import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import styled from 'styled-components';
import { useAuth } from '../hooks/useAuth';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input'; // We will create this file next

// This replaces PageWrapper for this specific page
const RegisterWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
`;

const Title = styled.h2`
  text-align: center;
  margin-bottom: ${({ theme }) => theme.spacing.large};
`;
const ErrorMessage = styled.p`
  color: ${({ theme }) => theme.colors.danger};
  font-size: 0.9rem;
  text-align: left;
  margin: -10px 0 10px 0;
`;
const Subtext = styled.p`
  text-align: center;
  margin-top: 1rem;
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const RegisterPage = () => {
    const [formData, setFormData] = useState({ email: '', password: '', phone_number: '', address: '' });
    const [errors, setErrors] = useState({});
    const { register } = useAuth();
    const navigate = useNavigate();

    const validate = () => {
        const newErrors = {};
        if (!/\S+@\S+\.\S+/.test(formData.email)) {
            newErrors.email = 'Please enter a valid email address.';
        }
        if (!/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/.test(formData.password)) {
            newErrors.password = 'Password must be 8+ characters with uppercase, lowercase, and a number.';
        }
        if (!formData.phone_number) newErrors.phone_number = 'Phone number is required.';
        if (!formData.address) newErrors.address = 'Ethereum address is required.';
        
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (validate()) {
            try {
                await register(formData);
                navigate('/login');
            } catch (err) {
                setErrors({ form: 'Registration failed. This email may already be in use.' });
            }
        }
    };

    return (
        <RegisterWrapper>
            <Card style={{width: '450px'}}>
                <Title>Create Your Secure Account</Title>
                <form onSubmit={handleSubmit}>
                    <Input name="email" type="email" placeholder="Email Address" onChange={handleChange} error={errors.email} />
                    {errors.email && <ErrorMessage>{errors.email}</ErrorMessage>}
                    
                    <Input name="password" type="password" placeholder="Password" onChange={handleChange} error={errors.password} />
                    {errors.password && <ErrorMessage>{errors.password}</ErrorMessage>}

                    <Input name="phone_number" type="text" placeholder="Phone Number (e.g., +91...)" onChange={handleChange} error={errors.phone_number} />
                    {errors.phone_number && <ErrorMessage>{errors.phone_number}</ErrorMessage>}

                    <Input name="address" type="text" placeholder="Your Ethereum Address (0x...)" onChange={handleChange} error={errors.address} />
                    {errors.address && <ErrorMessage>{errors.address}</ErrorMessage>}
                    
                    {errors.form && <ErrorMessage style={{textAlign: 'center'}}>{errors.form}</ErrorMessage>}
                    <Button type="submit">Create Account</Button>
                </form>
                <Subtext>Already have an account? <Link to="/login" style={{color: '#4a90e2'}}>Login here</Link></Subtext>
            </Card>
        </RegisterWrapper>
    );
};

export default RegisterPage;