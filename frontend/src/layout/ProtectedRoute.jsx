import { Navigate, Outlet } from 'react-router-dom';
import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Footer } from './Footer';
import { Navbar } from './Navbar';
import { Sidebar } from './Sidebar';
import { PageLoader } from '../components/ui/LoadingSpinner';

export function ProtectedRoute() {
  const { isAuthenticated, initializing } = useAuth();

  if (initializing) {
    return <PageLoader text="Checking session..." />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <DashboardLayout />;
}

export function DashboardLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-slate-950">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Navbar onMenuClick={() => setSidebarOpen(true)} />
        <main className="flex-1 overflow-y-auto">
          <div className="page-container animate-fade-in">
            <Outlet />
          </div>
        </main>
        <Footer />
      </div>
    </div>
  );
}

export function PublicRoute({ children }) {
  const { isAuthenticated, initializing, loading } = useAuth();

  if (initializing || loading) {
    return <PageLoader text="Loading..." />;
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}
