import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { Layout } from './components/Layout';
import { ProtectedRoute, AdminRoute } from './components/RouteGuards';

import { LandingPage } from './pages/LandingPage';
import { RegisterPage } from './pages/RegisterPage';
import { LoginPage } from './pages/LoginPage';
import { OnboardingPage } from './pages/OnboardingPage';
import { DashboardPage } from './pages/DashboardPage';
import { LibraryPage } from './pages/LibraryPage';
import { InterviewRoomPage } from './pages/InterviewRoomPage';
import { InterviewResultsPage } from './pages/InterviewResultsPage';
import { ResumePrepPage } from './pages/ResumePrepPage';
import { HRStudioPage } from './pages/HRStudioPage';
import { CompanyPrepPage } from './pages/CompanyPrepPage';
import { RoadmapPage } from './pages/RoadmapPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { SettingsPage } from './pages/SettingsPage';
import { AdminQuestionsPage } from './pages/AdminQuestionsPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <AuthProvider>
          <BrowserRouter>
            <Routes>
              {/* Public & App Shell */}
              <Route element={<Layout />}>
                {/* 1. Landing Page */}
                <Route path="/" element={<LandingPage />} />

                {/* 2. Register Page */}
                <Route path="/register" element={<RegisterPage />} />

                {/* 3. Login Page */}
                <Route path="/login" element={<LoginPage />} />

                {/* 4. Onboarding Page */}
                <Route
                  path="/onboarding"
                  element={
                    <ProtectedRoute>
                      <OnboardingPage />
                    </ProtectedRoute>
                  }
                />

                {/* 5. Dashboard */}
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute>
                      <DashboardPage />
                    </ProtectedRoute>
                  }
                />

                {/* 5b. Resume Analysis & Interview Prep */}
                <Route
                  path="/resume-prep"
                  element={
                    <ProtectedRoute>
                      <ResumePrepPage />
                    </ProtectedRoute>
                  }
                />

                {/* 6. Interview Preparation Library */}
                <Route path="/library" element={<LibraryPage />} />

                {/* 7. AI Mock Interview Room */}
                <Route
                  path="/interview/new"
                  element={
                    <ProtectedRoute>
                      <InterviewRoomPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/interview/:sessionId"
                  element={
                    <ProtectedRoute>
                      <InterviewRoomPage />
                    </ProtectedRoute>
                  }
                />

                {/* 8. Interview Results Page */}
                <Route
                  path="/interview/:sessionId/results"
                  element={
                    <ProtectedRoute>
                      <InterviewResultsPage />
                    </ProtectedRoute>
                  }
                />

                {/* 9. HR Answer Improvement Studio */}
                <Route
                  path="/hr-studio"
                  element={
                    <ProtectedRoute>
                      <HRStudioPage />
                    </ProtectedRoute>
                  }
                />

                {/* 10. Company-Specific Preparation */}
                <Route path="/company-prep" element={<CompanyPrepPage />} />
                <Route path="/company-prep/:slug" element={<CompanyPrepPage />} />

                {/* 11. Learning Roadmap */}
                <Route
                  path="/roadmap"
                  element={
                    <ProtectedRoute>
                      <RoadmapPage />
                    </ProtectedRoute>
                  }
                />

                {/* 12. Progress Analytics */}
                <Route
                  path="/analytics"
                  element={
                    <ProtectedRoute>
                      <AnalyticsPage />
                    </ProtectedRoute>
                  }
                />

                {/* 13. Profile & Settings */}
                <Route
                  path="/settings"
                  element={
                    <ProtectedRoute>
                      <SettingsPage />
                    </ProtectedRoute>
                  }
                />

                {/* 14. Admin Question Management */}
                <Route
                  path="/admin/questions"
                  element={
                    <AdminRoute>
                      <AdminQuestionsPage />
                    </AdminRoute>
                  }
                />

                {/* Fallback */}
                <Route path="*" element={<Navigate to="/" replace />} />
              </Route>
            </Routes>
          </BrowserRouter>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
};

export default App;
