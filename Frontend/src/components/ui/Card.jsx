import styled from 'styled-components';

const Card = styled.div`
  background: rgba(26, 26, 58, 0.6); /* Semi-transparent background */
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: ${({ theme }) => theme.borderRadius};
  border: 1px solid rgba(0, 245, 255, 0.2);
  padding: ${({ theme }) => theme.spacing.large};
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
  width: 100%;
  max-width: ${props => props.maxWidth || '500px'};
`;

export default Card;