import React, { useState } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { FiPhone, FiX } from 'react-icons/fi';
import Button from './Button';
import toast from 'react-hot-toast';

const Overlay = styled(motion.div)`
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
`;

const ModalCard = styled(motion.div)`
    background: ${({ theme }) => theme.colors.panel};
    backdrop-filter: blur(20px);
    border: 2px solid ${({ theme }) => theme.colors.border};
    border-radius: 24px;
    padding: ${({ theme }) => theme.spacing.xl};
    max-width: 400px;
    width: 90%;
    box-shadow: 0 20px 60px ${({ theme }) => theme.colors.shadow};
    position: relative;
`;

const CloseButton = styled.button`
    position: absolute;
    top: 16px;
    right: 16px;
    background: transparent;
    border: none;
    color: ${({ theme }) => theme.colors.textSecondary};
    cursor: pointer;
    padding: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: ${({ theme }) => theme.transition};

    &:hover {
        background: ${({ theme }) => theme.colors.border};
        color: ${({ theme }) => theme.colors.textPrimary};
    }
`;

const PhoneIcon = styled.div`
    width: 80px;
    height: 80px;
    background: ${({ theme }) => theme.colors.primaryGradient};
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 24px;
    animation: pulse 2s infinite;
`;

const Title = styled.h2`
    text-align: center;
    margin-bottom: 8px;
    font-size: 1.5rem;
`;

const Message = styled.p`
    text-align: center;
    color: ${({ theme }) => theme.colors.textSecondary};
    margin-bottom: 24px;
    line-height: 1.6;
`;

const KeypadGrid = styled.div`
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 24px 0;
`;

const KeyButton = styled(motion.button)`
    padding: 20px;
    background: ${({ theme }) => theme.colors.panelGlass};
    backdrop-filter: blur(10px);
    border: 2px solid ${({ theme }) => theme.colors.border};
    border-radius: 12px;
    color: ${({ theme }) => theme.colors.textPrimary};
    font-size: 1.5rem;
    font-weight: 600;
    cursor: pointer;
    transition: ${({ theme }) => theme.transition};

    &:hover {
        background: ${({ theme }) => theme.colors.primary};
        color: white;
        transform: scale(1.05);
    }
`;

const VoiceCallModal = ({ isOpen, onClose, transactionAmount, onConfirm }) => {
    const [pressed, setPressed] = useState(null);

    const handleKeyPress = (key) => {
        setPressed(key);
        
        if (key === '1') {
            toast.success('Transaction confirmed! Proceeding...');
            onConfirm('confirmed');
            setTimeout(onClose, 1500);
        } else if (key === '2') {
            toast.error('Transaction blocked for security!');
            onConfirm('blocked');
            setTimeout(onClose, 1500);
        } else if (key === '3') {
            toast('Initiating additional verification...');
            onConfirm('verify');
            setTimeout(onClose, 1500);
        }
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <Overlay
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    onClick={onClose}
                >
                    <ModalCard
                        initial={{ scale: 0.8, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0.8, opacity: 0 }}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <CloseButton onClick={onClose}>
                            <FiX size={24} />
                        </CloseButton>

                        <PhoneIcon>
                            <FiPhone size={40} color="white" />
                        </PhoneIcon>

                        <Title>Security Verification</Title>
                        <Message>
                            A high-risk transaction of <strong>₹{transactionAmount?.toLocaleString()}</strong> was detected.
                            <br /><br />
                            <strong>Press 1:</strong> I initiated this transaction<br />
                            <strong>Press 2:</strong> Block this transaction<br />
                            <strong>Press 3:</strong> Additional verification
                        </Message>

                        <KeypadGrid>
                            {[1, 2, 3].map((num) => (
                                <KeyButton
                                    key={num}
                                    whileTap={{ scale: 0.95 }}
                                    onClick={() => handleKeyPress(num.toString())}
                                >
                                    {num}
                                </KeyButton>
                            ))}
                        </KeypadGrid>
                    </ModalCard>
                </Overlay>
            )}
        </AnimatePresence>
    );
};

export default VoiceCallModal;
