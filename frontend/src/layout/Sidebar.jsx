import { NavLink, useNavigate } from 'react-router-dom';
import {
  FiBarChart2,
  FiFileText,
  FiGrid,
  FiLogOut,
  FiSettings,
  FiUpload,
  FiX,
} from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import { NAV_ITEMS } from '../utils/constants';

const ICON_MAP = {
  dashboard: FiGrid,
  analyze: FiUpload,
  history: FiFileText,
  settings: FiSettings,
};

export function Sidebar({ isOpen, onClose }) {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm lg:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      <aside
        className={`fixed inset-y-0 left-0 z-50 flex w-64 flex-col border-r border-slate-200/80 bg-white transition-transform duration-300 dark:border-slate-700/50 dark:bg-slate-900 lg:static lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex h-16 items-center justify-between border-b border-slate-200/80 px-5 dark:border-slate-700/50">
          <div className="flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-accent-500 text-white shadow-md">
              <FiBarChart2 className="h-5 w-5" />
            </div>
            <div>
              <p className="text-sm font-bold text-slate-800 dark:text-white">Resume AI</p>
              <p className="text-[10px] font-medium text-slate-400">Analyzer Pro</p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 lg:hidden hover:bg-slate-100 dark:hover:bg-slate-800"
            aria-label="Close menu"
          >
            <FiX className="h-5 w-5" />
          </button>
        </div>

        <nav className="flex-1 space-y-1 overflow-y-auto p-4">
          {NAV_ITEMS.map((item) => {
            const Icon = ICON_MAP[item.icon];
            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-medium transition-all duration-200 ${
                    isActive
                      ? 'bg-gradient-to-r from-brand-500 to-accent-500 text-white shadow-md'
                      : 'text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800'
                  }`
                }
              >
                <Icon className="h-5 w-5" />
                {item.label}
              </NavLink>
            );
          })}
        </nav>

        <div className="border-t border-slate-200/80 p-4 dark:border-slate-700/50">
          <div className="mb-3 rounded-xl bg-slate-50 p-3 dark:bg-slate-800/50">
            <p className="truncate text-sm font-semibold text-slate-800 dark:text-white">{user?.full_name}</p>
            <p className="truncate text-xs text-slate-500">{user?.email}</p>
          </div>
          <button
            type="button"
            onClick={handleLogout}
            className="flex w-full items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-medium text-red-500 transition-all hover:bg-red-50 dark:hover:bg-red-950/30"
          >
            <FiLogOut className="h-5 w-5" />
            Logout
          </button>
        </div>
      </aside>
    </>
  );
}
