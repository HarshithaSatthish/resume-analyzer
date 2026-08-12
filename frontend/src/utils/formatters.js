export function formatDate(dateString) {
  if (!dateString) return '—';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function formatFileSize(bytes) {
  if (!bytes || bytes === 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB'];
  const index = Math.floor(Math.log(bytes) / Math.log(1024));
  return `${(bytes / Math.pow(1024, index)).toFixed(1)} ${units[index]}`;
}

export function formatScore(score) {
  if (score == null || Number.isNaN(score)) return '0';
  return Math.round(score);
}

export function getScoreColor(score) {
  if (score >= 80) return 'text-emerald-500';
  if (score >= 60) return 'text-brand-500';
  if (score >= 40) return 'text-amber-500';
  return 'text-red-500';
}

export function getScoreBgColor(score) {
  if (score >= 80) return 'bg-emerald-500';
  if (score >= 60) return 'bg-brand-500';
  if (score >= 40) return 'bg-amber-500';
  return 'bg-red-500';
}

export function getScoreLabel(score) {
  if (score >= 80) return 'Excellent';
  if (score >= 60) return 'Good';
  if (score >= 40) return 'Average';
  return 'Needs Work';
}

export function truncateText(text, maxLength = 100) {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength)}...`;
}

export function capitalizeWords(str) {
  if (!str) return '';
  return str.replace(/\b\w/g, (char) => char.toUpperCase());
}
