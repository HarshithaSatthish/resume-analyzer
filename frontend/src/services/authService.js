import api from './api';

export async function registerUser({ full_name, email, password }) {
  const { data } = await api.post('/register', { full_name, email, password });
  return data;
}

export async function loginUser({ email, password }) {
  const { data } = await api.post('/login', { email, password });
  return data;
}

export async function logoutUser() {
  const { data } = await api.post('/logout');
  return data;
}

export async function getCurrentUser() {
  const { data } = await api.get('/me');
  return data;
}

export async function updateProfile({ full_name }) {
  const { data } = await api.put('/profile', { full_name });
  return data;
}

export async function updateSettings({ gemini_api_key }) {
  const { data } = await api.put('/settings', { gemini_api_key });
  return data;
}

export async function changePassword({ current_password, new_password }) {
  const { data } = await api.put('/password', { current_password, new_password });
  return data;
}
