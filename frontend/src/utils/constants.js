const PRODUCTION_API_URL = 'https://resume-analyzer-api-23f3.onrender.com/api';
const LOCAL_API_URL = 'http://localhost:8000/api';

function resolveApiUrl() {
  const envUrl = import.meta.env.VITE_API_URL;

  if (envUrl && !envUrl.includes('your-render-service')) {
    return envUrl;
  }

  if (typeof window !== 'undefined' && window.location.hostname.endsWith('.vercel.app')) {
    return PRODUCTION_API_URL;
  }

  return envUrl || LOCAL_API_URL;
}

export const API_URL = resolveApiUrl();

export const MAX_FILE_SIZE_MB = 5;
export const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;

export const ACCEPTED_FILE_TYPES = {
  'application/pdf': ['.pdf'],
};

export const STORAGE_KEYS = {
  TOKEN: 'resume_analyzer_token',
  USER: 'resume_analyzer_user',
  THEME: 'resume_analyzer_theme',
  GEMINI_KEY: 'resume_analyzer_gemini_key',
};

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  ANALYZE: '/analyze',
  HISTORY: '/history',
  REPORT: '/report/:id',
  SETTINGS: '/settings',
  ERROR: '/error',
};

export const SCORE_COLORS = {
  excellent: '#10b981',
  good: '#6366f1',
  average: '#f59e0b',
  poor: '#ef4444',
};

export const NAV_ITEMS = [
  { path: '/dashboard', label: 'Dashboard', icon: 'dashboard' },
  { path: '/analyze', label: 'Analyze', icon: 'analyze' },
  { path: '/history', label: 'History', icon: 'history' },
  { path: '/settings', label: 'Settings', icon: 'settings' },
];
