import { Toaster } from 'react-hot-toast';
import styled from 'styled-components';

const StyledToaster = styled(Toaster)`
    .toast {
        backdrop-filter: blur(20px);
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
`;

const Toast = () => (
    <StyledToaster
        position="top-right"
        toastOptions={{
            duration: 3000,
            style: {
                background: 'rgba(30, 30, 46, 0.95)',
                color: '#f7fafc',
                border: '1px solid rgba(139, 92, 246, 0.3)',
            },
            success: {
                iconTheme: {
                    primary: '#48bb78',
                    secondary: '#fff',
                },
            },
            error: {
                iconTheme: {
                    primary: '#f56565',
                    secondary: '#fff',
                },
            },
        }}
    />
);

export default Toast;
