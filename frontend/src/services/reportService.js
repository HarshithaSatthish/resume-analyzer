import api from './api';
import { API_URL } from '../utils/constants';
import { getToken } from '../utils/storage';

export async function getHistory(search = '') {
  const params = search ? { search } : {};
  const { data } = await api.get('/history', { params });
  return data;
}

export async function getReport(reportId) {
  const { data } = await api.get(`/report/${reportId}`);
  return data;
}

export async function deleteReport(reportId) {
  const { data } = await api.delete(`/report/${reportId}`);
  return data;
}

export function getDownloadUrl(reportId) {
  return `${API_URL}/download/${reportId}`;
}

export async function downloadReport(reportId, filename = 'resume-report.pdf') {
  const token = getToken();
  const response = await fetch(`${API_URL}/download/${reportId}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || errorData.message || 'Failed to download report.');
  }

  const contentType = response.headers.get('content-type') || '';
  if (!contentType.includes('application/pdf')) {
    throw new Error('Server did not return a valid PDF file.');
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}

export async function getHealth() {
  const { data } = await api.get('/health');
  return data;
}
