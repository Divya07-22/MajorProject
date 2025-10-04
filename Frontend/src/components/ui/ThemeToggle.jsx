// src/components/ui/ThemeToggle.jsx

import React from 'react';
import styled from 'styled-components';
import { FiSun, FiMoon } from 'react-icons/fi';

const ToggleButton = styled.button`
    background: transparent;
    border: 1px solid ${({ theme }) => theme.colors.border};
    color: ${({ theme }) => theme.colors.textSecondary};
    padding: 8px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;

    &:hover {
        color: ${({ theme }) => theme.colors.textPrimary};
        border-color: ${({ theme }) => theme.colors.primary};
    }
`;

const ThemeToggle = ({ theme, toggleTheme }) => {
    return (
        <ToggleButton onClick={toggleTheme}>
            {theme === 'dark' ? <FiSun size={20} /> : <FiMoon size={20} />}
        </ToggleButton>
    );
};

export default ThemeToggle;