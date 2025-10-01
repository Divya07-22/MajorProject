// File: src/styles/theme.js

export const theme = {
  colors: {
    background: '#0a0a1a', // Deep charcoal/navy blue
    primary: '#00f5ff',     // Electric cyan for highlights and primary actions
    secondary: '#1a1a3a',   // Slightly lighter navy for cards and panels
    text: '#e0e0e0',        // Soft white for text
    textSecondary: '#a0a0c0', // Lighter gray for subtitles
    accent: '#ffab00',      // Warm amber for warnings or secondary highlights
    danger: '#ff1744',      // Deep red for critical alerts
    success: '#00e676',     // Bright green for success messages
    glow: 'rgba(0, 245, 255, 0.5)', // Glow effect color for the primary cyan
  },
  fonts: {
    primary: "'Poppins', sans-serif",
  },
  fontSizes: {
    small: '0.8rem',
    medium: '1rem',
    large: '1.5rem',
    xlarge: '2.5rem',
  },
  spacing: {
    small: '8px',
    medium: '16px',
    large: '32px',
  },
  shadows: {
    glow: '0 0 15px rgba(0, 245, 255, 0.6)',
  },
  borderRadius: '12px',
};