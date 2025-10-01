// File: src/styles/GlobalStyles.js

import { createGlobalStyle } from 'styled-components';

const GlobalStyles = createGlobalStyle`
  *,
  *::before,
  *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    background-color: ${({ theme }) => theme.colors.background};
    color: ${({ theme }) => theme.colors.text};
    font-family: ${({ theme }) => theme.fonts.primary};
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    overflow-x: hidden;
  }

  h1, h2, h3, h4, h5, h6 {
    color: ${({ theme }) => theme.colors.primary};
    font-weight: 600;
  }

  a {
    color: ${({ theme }) => theme.colors.primary};
    text-decoration: none;
    transition: color 0.3s ease-in-out;

    &:hover {
      color: ${({ theme }) => theme.colors.accent};
    }
  }

  /* Custom scrollbar for a more modern look */
  ::-webkit-scrollbar {
    width: 8px;
  }
  ::-webkit-scrollbar-track {
    background: ${({ theme }) => theme.colors.secondary};
  }
  ::-webkit-scrollbar-thumb {
    background: ${({ theme }) => theme.colors.primary};
    border-radius: 4px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: ${({ theme }) => theme.colors.accent};
  }
`;

export default GlobalStyles;