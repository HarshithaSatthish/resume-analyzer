import axios from 'axios';
import { API_URL } from '../utils/constants';
import { getToken, clearAuthStorage } from '../utils/storage';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000,
});

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.message ||
      error.response?.data?.detail ||
      error.message ||
      'An unexpected error occurred.';

    if (error.response?.status === 401) {
      const requestUrl = error.config?.url || '';
      const isAuthRequest = ['/login', '/register'].some((path) => requestUrl.includes(path));
      clearAuthStorage();
      if (!isAuthRequest && window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }

    return Promise.reject(new Error(typeof message === 'string' ? message : JSON.stringify(message)));
  }
);

export default api;

export function getErrorMessage(error) {
  if (error instanceof Error) return error.message;
  return 'An unexpected error occurred.';
}
