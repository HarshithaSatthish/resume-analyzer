import { STORAGE_KEYS } from './constants';

export function getToken() {
  return localStorage.getItem(STORAGE_KEYS.TOKEN);
}

export function setToken(token) {
  localStorage.setItem(STORAGE_KEYS.TOKEN, token);
}

export function removeToken() {
  localStorage.removeItem(STORAGE_KEYS.TOKEN);
}

export function getUser() {
  const raw = localStorage.getItem(STORAGE_KEYS.USER);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function setUser(user) {
  localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
}

export function removeUser() {
  localStorage.removeItem(STORAGE_KEYS.USER);
}

export function getTheme() {
  return localStorage.getItem(STORAGE_KEYS.THEME) || 'light';
}

export function setTheme(theme) {
  localStorage.setItem(STORAGE_KEYS.THEME, theme);
}

export function getGeminiKey() {
  return localStorage.getItem(STORAGE_KEYS.GEMINI_KEY) || '';
}

export function setGeminiKey(key) {
  if (key) {
    localStorage.setItem(STORAGE_KEYS.GEMINI_KEY, key);
  } else {
    localStorage.removeItem(STORAGE_KEYS.GEMINI_KEY);
  }
}

export function clearAuthStorage() {
  removeToken();
  removeUser();
}
