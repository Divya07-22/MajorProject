import React from 'react';
import styled from 'styled-components';
import { FiSun, FiMoon } from 'react-icons/fi';
import { motion } from 'framer-motion';

const ToggleButton = styled(motion.button)`
    background: ${({ theme }) => theme.colors.panelGlass};
    backdrop-filter: blur(10px);
    border: 2px solid ${({ theme }) => theme.colors.border};
    color: ${({ theme }) => theme.colors.textPrimary};
    padding: 12px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: ${({ theme }) => theme.transition};
    box-shadow: 0 4px 12px ${({ theme }) => theme.colors.shadow};

    &:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 16px ${({ theme }) => theme.colors.shadow};
    }
`;

const ThemeToggle = ({ theme, toggleTheme }) => {
    return (
        <ToggleButton
            onClick={toggleTheme}
            whileTap={{ scale: 0.9 }}
            whileHover={{ rotate: 180 }}
            transition={{ duration: 0.3 }}
        >
            {theme === 'dark' ? <FiSun size={20} /> : <FiMoon size={20} />}
        </ToggleButton>
    );
};

export default ThemeToggle;
