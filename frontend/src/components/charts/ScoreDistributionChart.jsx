import { Bar } from 'react-chartjs-2';
import { useChartTheme } from '../../hooks/useChartTheme';
import { ChartEmptyState } from './ChartCard';
import './chartRegistry';

const BUCKETS = [
  { label: '0-40', min: 0, max: 40 },
  { label: '40-60', min: 40, max: 60 },
  { label: '60-80', min: 60, max: 80 },
  { label: '80-100', min: 80, max: 100.1 },
];

export function ScoreDistributionChart({ reports = [], className = '' }) {
  const { theme, baseOptions } = useChartTheme();

  if (!reports.length) {
    return <ChartEmptyState message="No score distribution yet" className={className} />;
  }

  const counts = BUCKETS.map(({ min, max }) =>
    reports.filter((report) => report.overall_score >= min && report.overall_score < max).length
  );

  const data = {
    labels: BUCKETS.map((bucket) => bucket.label),
    datasets: [
      {
        label: 'Reports',
        data: counts,
        backgroundColor: ['#ef4444aa', '#f59e0baa', '#6366f1aa', '#10b981aa'],
        borderColor: ['#ef4444', '#f59e0b', '#6366f1', '#10b981'],
        borderWidth: 1,
        borderRadius: 8,
      },
    ],
  };

  const options = baseOptions({
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (ctx) => ` ${ctx.raw} report${ctx.raw === 1 ? '' : 's'}`,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: { stepSize: 1, color: theme.muted },
        grid: { color: theme.grid },
      },
      x: {
        grid: { display: false },
        ticks: { color: theme.muted },
      },
    },
  });

  return (
    <div className={`h-56 ${className}`}>
      <Bar data={data} options={options} />
    </div>
  );
}
