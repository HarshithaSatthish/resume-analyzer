import api from './api';

export async function uploadResume(file, onProgress) {
  const formData = new FormData();
  formData.append('file', file);

  const { data } = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (event) => {
      if (onProgress && event.total) {
        const percent = Math.round((event.loaded * 100) / event.total);
        onProgress(percent);
      }
    },
  });
  return data;
}

export async function parseResume(fileId) {
  const { data } = await api.post('/parse', { file_id: fileId });
  return data;
}

export async function generateAIFeedback(fileId, jobDescription = null) {
  const payload = { file_id: fileId };
  if (jobDescription) payload.job_description = jobDescription;
  const { data } = await api.post('/ai/feedback', payload);
  return data;
}

export async function calculateATSScore(fileId) {
  const { data } = await api.post('/ats', { file_id: fileId });
  return data;
}

export async function analyzeResume(fileId) {
  const { data } = await api.post('/analyze', { file_id: fileId });
  return data;
}

export async function compareJobDescription(reportId, jobDescription) {
  const { data } = await api.post('/compare', {
    report_id: reportId,
    job_description: jobDescription,
  });
  return data;
}
