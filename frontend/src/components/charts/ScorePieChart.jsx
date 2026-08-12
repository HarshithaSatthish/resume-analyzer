import { Pie } from 'react-chartjs-2';
import { useChartTheme } from '../../hooks/useChartTheme';
import { CHART_PALETTE, getScoreLabels, getScoreValues } from '../../utils/chartTheme';
import './chartRegistry';

export function ScorePieChart({ scores, className = '' }) {
  const { theme, baseOptions } = useChartTheme();

  if (!scores) return null;

  const data = {
    labels: getScoreLabels(),
    datasets: [
      {
        data: getScoreValues(scores),
        backgroundColor: CHART_PALETTE,
        borderWidth: 2,
        borderColor: theme.border,
      },
    ],
  };

  const options = baseOptions({
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: theme.text,
          padding: 12,
          usePointStyle: true,
          pointStyle: 'circle',
          font: { size: 11 },
        },
      },
      tooltip: {
        callbacks: {
          label: (ctx) => ` ${ctx.label}: ${Math.round(ctx.raw)}%`,
        },
      },
    },
  });

  return (
    <div className={`h-72 ${className}`}>
      <Pie data={data} options={options} />
    </div>
  );
}
