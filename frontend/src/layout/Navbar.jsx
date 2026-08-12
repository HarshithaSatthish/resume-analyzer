import { Link, useLocation } from 'react-router-dom';
import { FiMenu, FiMoon, FiSun, FiBell } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

export function Navbar({ onMenuClick }) {
  const { user } = useAuth();
  const { isDark, toggleTheme } = useTheme();
  const location = useLocation();

  const pageTitles = {
    '/dashboard': 'Dashboard',
    '/analyze': 'Analyze Resume',
    '/history': 'Report History',
    '/settings': 'Settings',
  };

  const reportMatch = location.pathname.match(/^\/report\//);
  const pageTitle = reportMatch ? 'Report Details' : pageTitles[location.pathname] || 'AI Resume Analyzer';

  return (
    <header className="sticky top-0 z-30 border-b border-slate-200/80 bg-white/80 backdrop-blur-xl dark:border-slate-700/50 dark:bg-slate-900/80">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6">
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={onMenuClick}
            className="rounded-lg p-2 text-slate-500 transition-colors hover:bg-slate-100 lg:hidden dark:hover:bg-slate-800"
            aria-label="Open menu"
          >
            <FiMenu className="h-5 w-5" />
          </button>
          <div>
            <h1 className="text-lg font-bold text-slate-800 dark:text-white">{pageTitle}</h1>
            <p className="hidden text-xs text-slate-500 sm:block">
              Welcome back, {user?.full_name?.split(' ')[0] || 'User'}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={toggleTheme}
            className="rounded-xl p-2.5 text-slate-500 transition-all hover:bg-slate-100 hover:text-brand-600 dark:hover:bg-slate-800 dark:hover:text-brand-400"
            aria-label="Toggle theme"
          >
            {isDark ? <FiSun className="h-5 w-5" /> : <FiMoon className="h-5 w-5" />}
          </button>

          <button
            type="button"
            className="hidden rounded-xl p-2.5 text-slate-500 transition-all hover:bg-slate-100 sm:block dark:hover:bg-slate-800"
            aria-label="Notifications"
          >
            <FiBell className="h-5 w-5" />
          </button>

          <Link
            to="/settings"
            className="flex items-center gap-2 rounded-xl border border-slate-200 px-3 py-1.5 transition-all hover:border-brand-300 hover:bg-brand-50 dark:border-slate-600 dark:hover:border-brand-500 dark:hover:bg-slate-800"
          >
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-brand-500 to-accent-500 text-sm font-bold text-white">
              {user?.full_name?.charAt(0)?.toUpperCase() || 'U'}
            </div>
            <span className="hidden text-sm font-medium text-slate-700 md:block dark:text-slate-200">
              {user?.full_name?.split(' ')[0]}
            </span>
          </Link>
        </div>
      </div>
    </header>
  );
}
