import React from "react";
import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";

// Layouts
import MainLayout from "./layouts/MainLayout";
import AdminLayout from "./layouts/AdminLayout";

// Public & Student Pages
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ExplorePage from "./pages/ExplorePage";
import ItemDetailsPage from "./pages/ItemDetailsPage";
import StudentDashboard from "./pages/StudentDashboard";
import ReportLostPage from "./pages/ReportLostPage";
import ReportFoundPage from "./pages/ReportFoundPage";
import ClaimItemPage from "./pages/ClaimItemPage";
import ClaimSuccessPage from "./pages/ClaimSuccessPage";
import TrackClaimsPage from "./pages/TrackClaimsPage";
import MyReportsAndClaimsPage from "./pages/MyReportsAndClaimsPage";
import NotificationsPage from "./pages/NotificationsPage";
import ProfilePage from "./pages/ProfilePage";

// Admin Pages
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminItemsPage from "./pages/admin/AdminItemsPage";
import AdminClaimsPage from "./pages/admin/AdminClaimsPage";
import AdminAuditLogsPage from "./pages/admin/AdminAuditLogsPage";

// Root Gate: Without login, no access - immediately redirects to /login.
// If already logged in, takes admin to /admin and student to /explore.
const RootRedirect = () => {
  const { isAuthenticated, user, loading } = useAuth();
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  if (user?.role === "admin") {
    return <Navigate to="/admin" replace />;
  }
  return <Navigate to="/explore" replace />;
};

// Protected Route Guard
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return children;
};

export const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public & Student Routes in MainLayout */}
          <Route element={<MainLayout />}>
            {/* Root redirects to Login (or Dashboard/Admin if already authenticated) */}
            <Route path="/" element={<RootRedirect />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            {/* Protected Student & Exploration Routes - Require Login */}
            <Route
              path="/explore"
              element={
                <ProtectedRoute>
                  <ExplorePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/items/:id"
              element={
                <ProtectedRoute>
                  <ItemDetailsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <StudentDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/report-lost"
              element={
                <ProtectedRoute>
                  <ReportLostPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/report-found"
              element={
                <ProtectedRoute>
                  <ReportFoundPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/claims/new/:id"
              element={
                <ProtectedRoute>
                  <ClaimItemPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/claims/success/:claimId"
              element={
                <ProtectedRoute>
                  <ClaimSuccessPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/my-claims"
              element={
                <ProtectedRoute>
                  <TrackClaimsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/claims/track"
              element={
                <ProtectedRoute>
                  <TrackClaimsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/claims/:id"
              element={
                <ProtectedRoute>
                  <ClaimSuccessPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/my-reports"
              element={
                <ProtectedRoute>
                  <MyReportsAndClaimsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/notifications"
              element={
                <ProtectedRoute>
                  <NotificationsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />
          </Route>

          {/* Admin Portal in AdminLayout */}
          <Route path="/admin" element={<AdminLayout />}>
            <Route index element={<AdminDashboard />} />
            <Route path="items" element={<AdminItemsPage />} />
            <Route path="claims" element={<AdminClaimsPage />} />
            <Route path="audit-logs" element={<AdminAuditLogsPage />} />
          </Route>

          {/* 404 Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
