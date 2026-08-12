import { Bar } from 'react-chartjs-2';
import { useChartTheme } from '../../hooks/useChartTheme';
import { CHART_PALETTE, getScoreLabels, getScoreValues } from '../../utils/chartTheme';
import './chartRegistry';

export function ScoreBarChart({ scores, className = '' }) {
  const { theme, baseOptions } = useChartTheme();

  if (!scores) return null;

  const data = {
    labels: getScoreLabels(),
    datasets: [
      {
        label: 'ATS Score',
        data: getScoreValues(scores),
        backgroundColor: CHART_PALETTE.map((color) => `${color}cc`),
        borderColor: CHART_PALETTE,
        borderWidth: 1,
        borderRadius: 8,
        borderSkipped: false,
      },
    ],
  };

  const options = baseOptions({
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (ctx) => ` Score: ${Math.round(ctx.raw)}%`,
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
        ticks: { color: theme.muted, font: { size: 10 } },
      },
    },
  });

  return (
    <div className={`h-72 ${className}`}>
      <Bar data={data} options={options} />
    </div>
  );
}
