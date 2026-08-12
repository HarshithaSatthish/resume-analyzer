import { Bar } from 'react-chartjs-2';
import { useChartTheme } from '../../hooks/useChartTheme';
import { ChartEmptyState } from './ChartCard';
import './chartRegistry';

export function JobMatchChart({ comparison, className = '' }) {
  const { theme, baseOptions } = useChartTheme();

  if (!comparison) {
    return <ChartEmptyState message="Run a job comparison to see skill match chart" className={className} />;
  }

  const matched = comparison.matched_skills?.length || 0;
  const missing = comparison.missing_skills?.length || 0;

  const data = {
    labels: ['Matched Skills', 'Missing Skills'],
    datasets: [
      {
        label: 'Skill Count',
        data: [matched, missing],
        backgroundColor: ['#10b981cc', '#ef4444cc'],
        borderColor: ['#10b981', '#ef4444'],
        borderWidth: 1,
        borderRadius: 8,
      },
    ],
  };

  const options = baseOptions({
    indexAxis: 'y',
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          afterLabel: () => `Match: ${Math.round(comparison.match_percentage)}%`,
        },
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        ticks: { stepSize: 1, color: theme.muted },
        grid: { color: theme.grid },
      },
      y: {
        grid: { display: false },
        ticks: { color: theme.text },
      },
    },
  });

  return (
    <div className={`h-48 ${className}`}>
      <Bar data={data} options={options} />
    </div>
  );
}
