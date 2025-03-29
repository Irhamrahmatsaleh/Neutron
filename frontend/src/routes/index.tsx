import HomePage from '../pages/home';
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import WalletPage from '../pages/wallet';
import Layout from '../layouts/Layout';
import ProfilePage from '../pages/profile';
import NotificationsPage from '../pages/notifications';

const AppRoutes: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/wallet" element={<WalletPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/notifications" element={<NotificationsPage />} />
          {/* Tambahkan rute lainnya di sini */}
        </Routes>
      </Layout>
    </Router>
  );
};

export default AppRoutes;
