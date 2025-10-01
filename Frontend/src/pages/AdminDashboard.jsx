import React from 'react';
import styled from 'styled-components';
import PageWrapper from '../components/layout/PageWrapper';
import Header from '../components/layout/Header';
import LiveTransactionFeed from '../components/admin/LiveTransactionFeed';
import FraudLogTable from '../components/admin/FraudLogTable';

const AdminContainer = styled.div`
  padding-top: 100px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing.large};
`;

const Title = styled.h2`
  text-align: center;
`;

const AdminDashboard = () => {
  return (
    <>
      <Header />
      <PageWrapper>
        <AdminContainer>
          <Title>Admin Mission Control</Title>
          <LiveTransactionFeed />
          <FraudLogTable />
        </AdminContainer>
      </PageWrapper>
    </>
  );
};

export default AdminDashboard;