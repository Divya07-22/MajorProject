import styled from 'styled-components';

const PageWrapper = styled.main`
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: ${({ theme }) => theme.spacing.large};
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

export default PageWrapper;