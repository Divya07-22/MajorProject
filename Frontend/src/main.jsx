// src/main.jsx

import React, { useState, useMemo } from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { ThemeProvider } from 'styled-components';
import { lightTheme, darkTheme } from './styles/theme';
import { AuthProvider } from './contexts/AuthContext';
import { BrowserRouter as Router } from 'react-router-dom';

const AppWrapper = () => {
    const [theme, setTheme] = useState('dark');

    const toggleTheme = () => {
        setTheme(theme === 'dark' ? 'light' : 'dark');
    };

    // This makes sure the theme object doesn't get recreated on every render
    const currentTheme = useMemo(() => (theme === 'dark' ? darkTheme : lightTheme), [theme]);

    return (
        <ThemeProvider theme={currentTheme}>
            <AuthProvider>
                <Router>
                    {/* Pass theme and toggleTheme down to the App */}
                    <App theme={theme} toggleTheme={toggleTheme} />
                </Router>
            </AuthProvider>
        </ThemeProvider>
    );
};

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <AppWrapper />
    </React.StrictMode>
);