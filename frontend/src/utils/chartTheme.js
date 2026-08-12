export const CHART_PALETTE = [
  '#6366f1',
  '#8b5cf6',
  '#3b82f6',
  '#06b6d4',
  '#10b981',
  '#f59e0b',
  '#ec4899',
  '#14b8a6',
  '#f97316',
  '#a855f7',
];

export const SCORE_METRICS = [
  { key: 'formatting_score', label: 'Formatting', weight: '15%' },
  { key: 'keyword_score', label: 'Keywords', weight: '10%' },
  { key: 'skill_score', label: 'Skills', weight: '25%' },
  { key: 'project_score', label: 'Projects', weight: '15%' },
  { key: 'education_score', label: 'Education', weight: '10%' },
  { key: 'experience_score', label: 'Experience', weight: '20%' },
  { key: 'readability_score', label: 'Readability', weight: '5%' },
];

export function getScoreColorValue(score) {
  if (score >= 80) return '#10b981';
  if (score >= 60) return '#6366f1';
  if (score >= 40) return '#f59e0b';
  return '#ef4444';
}

export function getScoreValues(scores) {
  if (!scores) return [];
  return SCORE_METRICS.map(({ key }) => scores[key] ?? 0);
}

export function getScoreLabels() {
  return SCORE_METRICS.map(({ label }) => label);
}

export function getChartTheme(isDark) {
  return {
    text: isDark ? '#e2e8f0' : '#334155',
    muted: isDark ? '#94a3b8' : '#64748b',
    grid: isDark ? 'rgba(148, 163, 184, 0.12)' : 'rgba(148, 163, 184, 0.25)',
    border: isDark ? '#1e293b' : '#ffffff',
    tooltipBg: isDark ? '#0f172a' : '#ffffff',
    tooltipBorder: isDark ? '#334155' : '#e2e8f0',
  };
}

export function buildBaseOptions(isDark, overrides = {}) {
  const theme = getChartTheme(isDark);
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: theme.text,
          usePointStyle: true,
          padding: 14,
          font: { size: 11 },
        },
      },
      tooltip: {
        backgroundColor: theme.tooltipBg,
        titleColor: theme.text,
        bodyColor: theme.muted,
        borderColor: theme.tooltipBorder,
        borderWidth: 1,
        padding: 10,
        cornerRadius: 8,
      },
    },
    ...overrides,
  };
}
