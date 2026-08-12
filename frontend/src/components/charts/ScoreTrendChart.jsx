import { Line } from 'react-chartjs-2';
import { useChartTheme } from '../../hooks/useChartTheme';
import { ChartEmptyState } from './ChartCard';
import './chartRegistry';

export function ScoreTrendChart({ reports = [], className = '' }) {
  const { theme, baseOptions } = useChartTheme();

  if (!reports.length) {
    return <ChartEmptyState message="Analyze resumes to see score trends" className={className} />;
  }

  const sorted = [...reports].sort(
    (a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
  );

  const labels = sorted.map((report) => {
    const date = new Date(report.created_at);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  });

  const values = sorted.map((report) => Math.round(report.overall_score));

  const data = {
    labels,
    datasets: [
      {
        label: 'ATS Score',
        data: values,
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99, 102, 241, 0.15)',
        fill: true,
        tension: 0.35,
        pointBackgroundColor: '#6366f1',
        pointBorderColor: theme.border,
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
      },
    ],
  };

  const options = baseOptions({
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (ctx) => ` ATS Score: ${ctx.raw}%`,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        grid: { color: theme.grid },
        ticks: { color: theme.muted, callback: (v) => `${v}%` },
      },
      x: {
        grid: { display: false },
        ticks: { color: theme.muted, maxRotation: 45, minRotation: 0 },
      },
    },
  });

  return (
    <div className={`h-64 ${className}`}>
      <Line data={data} options={options} />
    </div>
  );
}
