import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useAuth } from '../hooks/useAuth';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import PasswordStrengthMeter from '../components/ui/PasswordStrengthMeter';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import toast from 'react-hot-toast';
import { validateEmail, validatePassword, validatePhone, validateEthAddress } from '../utils/validation';

const RegisterWrapper = styled.div`
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
`;

const FormCard = styled(Card)`
    width: 100%;
    max-width: 500px;
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
    font-size: 0.9rem;
    margin-top: -8px;
    margin-bottom: 12px;
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

const RegisterPage = () => {
    const [formData, setFormData] = useState({ 
        email: '', 
        password: '', 
        phone_number: '', 
        address: '' 
    });
    const [errors, setErrors] = useState({});
    const [touched, setTouched] = useState({});
    const [loading, setLoading] = useState(false);
    const { register } = useAuth();
    const navigate = useNavigate();

    const validateField = (name, value) => {
        switch(name) {
            case 'email':
                return validateEmail(value) ? '' : 'Please enter a valid email address';
            case 'password':
                return validatePassword(value) 
                    ? '' 
                    : 'Password must be 8+ characters with uppercase, lowercase, number & special character';
            case 'phone_number':
                return validatePhone(value) 
                    ? '' 
                    : 'Phone must be in format: +91XXXXXXXXXX';
            case 'address':
                return validateEthAddress(value) 
                    ? '' 
                    : 'Ethereum address must start with 0x followed by 40 hex characters';
            default:
                return '';
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        
        // Real-time validation
        if (touched[name]) {
            const error = validateField(name, value);
            setErrors(prev => ({ ...prev, [name]: error }));
        }
    };

    const handleBlur = (e) => {
        const { name, value } = e.target;
        setTouched(prev => ({ ...prev, [name]: true }));
        const error = validateField(name, value);
        setErrors(prev => ({ ...prev, [name]: error }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Validate all fields
        const newErrors = {};
        Object.keys(formData).forEach(key => {
            const error = validateField(key, formData[key]);
            if (error) newErrors[key] = error;
        });

        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            setTouched({ email: true, password: true, phone_number: true, address: true });
            toast.error('Please fix all errors before submitting');
            return;
        }

        setLoading(true);
        try {
            await register(formData);
            toast.success('Account created successfully! Please login.');
            navigate('/login');
        } catch (err) {
            toast.error(err.response?.data?.error || 'Registration failed. Email may already exist.');
        } finally {
            setLoading(false);
        }
    };

    const isFieldValid = (name) => touched[name] && !errors[name] && formData[name];

    return (
        <RegisterWrapper>
            <FormCard
                as={motion.div}
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.5 }}
            >
                <Title>Create Your Account</Title>
                <form onSubmit={handleSubmit}>
                    <Input 
                        name="email" 
                        type="email" 
                        placeholder="Email Address" 
                        value={formData.email}
                        onChange={handleChange}
                        onBlur={handleBlur}
                        error={touched.email && errors.email}
                        valid={isFieldValid('email')}
                    />
                    {touched.email && errors.email && (
                        <ErrorMessage
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                        >
                            {errors.email}
                        </ErrorMessage>
                    )}

                    <Input 
                        name="password" 
                        type="password" 
                        placeholder="Password" 
                        value={formData.password}
                        onChange={handleChange}
                        onBlur={handleBlur}
                        error={touched.password && errors.password}
                        valid={isFieldValid('password')}
                    />
                    <PasswordStrengthMeter password={formData.password} />
                    {touched.password && errors.password && (
                        <ErrorMessage
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                        >
                            {errors.password}
                        </ErrorMessage>
                    )}

                    <Input 
                        name="phone_number" 
                        type="text" 
                        placeholder="Phone Number (+91XXXXXXXXXX)" 
                        value={formData.phone_number}
                        onChange={handleChange}
                        onBlur={handleBlur}
                        error={touched.phone_number && errors.phone_number}
                        valid={isFieldValid('phone_number')}
                    />
                    {touched.phone_number && errors.phone_number && (
                        <ErrorMessage
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                        >
                            {errors.phone_number}
                        </ErrorMessage>
                    )}

                    <Input 
                        name="address" 
                        type="text" 
                        placeholder="Ethereum Address (0x...)" 
                        value={formData.address}
                        onChange={handleChange}
                        onBlur={handleBlur}
                        error={touched.address && errors.address}
                        valid={isFieldValid('address')}
                    />
                    {touched.address && errors.address && (
                        <ErrorMessage
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                        >
                            {errors.address}
                        </ErrorMessage>
                    )}

                    <Button type="submit" disabled={loading}>
                        {loading ? <LoadingSpinner size="24px" /> : 'Create Account'}
                    </Button>
                </form>
                <Subtext>
                    Already have an account? <StyledLink to="/login">Login here</StyledLink>
                </Subtext>
            </FormCard>
        </RegisterWrapper>
    );
};

export default RegisterPage;
