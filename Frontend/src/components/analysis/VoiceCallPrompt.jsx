import React from 'react';
import styled from 'styled-components';

const PromptWrapper = styled.div`
  margin-top: ${({ theme }) => theme.spacing.large};
  padding: ${({ theme }) => theme.spacing.medium};
  border: 1px solid ${({ theme }) => theme.colors.accent};
  border-radius: ${({ theme }) => theme.borderRadius};
  background-color: rgba(255, 171, 0, 0.1);
`;

const PromptTitle = styled.h4`
  color: ${({ theme }) => theme.colors.accent};
  margin-bottom: ${({ theme }) => theme.spacing.small};
  text-align: center;
`;

const PromptText = styled.p`
  text-align: center;
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const VoiceCallPrompt = () => (
  <PromptWrapper>
    <PromptTitle>ACTION REQUIRED</PromptTitle>
    <PromptText>
      A security voice call has been initiated to your registered phone number.
      Please answer to confirm or block this transaction.
    </PromptText>
  </PromptWrapper>
);

export default VoiceCallPrompt;