import React from 'react';
import styled from 'styled-components';
import { getPasswordStrength } from '../../utils/validation';

const MeterWrapper = styled.div`
    margin: 8px 0;
`;

const MeterBar = styled.div`
    height: 4px;
    background: ${({ theme }) => theme.colors.border};
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 4px;
`;

const MeterFill = styled.div`
    height: 100%;
    width: ${({ strength }) => 
        strength === 'weak' ? '33%' : 
        strength === 'medium' ? '66%' : '100%'};
    background: ${({ color }) => color};
    transition: all 0.3s ease;
`;

const MeterLabel = styled.span`
    font-size: 0.85rem;
    color: ${({ color }) => color};
    font-weight: 500;
`;

const PasswordStrengthMeter = ({ password }) => {
    if (!password) return null;
    
    const { level, color } = getPasswordStrength(password);
    
    return (
        <MeterWrapper>
            <MeterBar>
                <MeterFill strength={level} color={color} />
            </MeterBar>
            <MeterLabel color={color}>
                Password strength: {level}
            </MeterLabel>
        </MeterWrapper>
    );
};

export default PasswordStrengthMeter;
