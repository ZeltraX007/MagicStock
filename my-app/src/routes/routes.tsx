// src/routes.tsx
import { Routes, Route } from 'react-router-dom';
import Dashboard from '../pages/Dashboard';
import LandingPage from '../pages/Landing';
import AboutPage from '../pages/About';
import HowItWorksPage from '../pages/HowItWorks';
import PrivacyPage from '../pages/Privacy';
import TermsPage from '../pages/Terms';
import ContactPage from '../pages/Contact';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/home" element={<LandingPage />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/about" element={<AboutPage />} />
      <Route path="/how-to-invest" element={<HowItWorksPage />} />
      <Route path="/privacy" element={<PrivacyPage />} />
      <Route path="/terms" element={<TermsPage />} />
      <Route path="/contact" element={<ContactPage />} />
    </Routes>
  );
};

export default AppRoutes;