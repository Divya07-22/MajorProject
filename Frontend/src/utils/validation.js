// Strong validation utilities

export const validateEmail = (email) => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
};

export const validatePassword = (password) => {
    // At least 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$/;
    return regex.test(password);
};

export const getPasswordStrength = (password) => {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[@$!%*?&#]/.test(password)) strength++;
    
    if (strength <= 2) return { level: 'weak', color: '#f56565' };
    if (strength <= 4) return { level: 'medium', color: '#ed8936' };
    return { level: 'strong', color: '#48bb78' };
};

export const validatePhone = (phone) => {
    // Indian phone: +91XXXXXXXXXX
    const regex = /^\+91[6-9]\d{9}$/;
    return regex.test(phone);
};

export const validateEthAddress = (address) => {
    // 0x followed by 40 hex characters
    const regex = /^0x[a-fA-F0-9]{40}$/;
    return regex.test(address);
};

export const validateAmount = (amount) => {
    const num = parseFloat(amount);
    return !isNaN(num) && num > 0 && num <= 10000000; // Max 1 crore
};
