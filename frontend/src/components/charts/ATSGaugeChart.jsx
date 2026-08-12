import { Doughnut } from 'react-chartjs-2';
import { useChartTheme } from '../../hooks/useChartTheme';
import { getScoreColorValue } from '../../utils/chartTheme';
import { getScoreLabel } from '../../utils/formatters';
import './chartRegistry';

export function ATSGaugeChart({ score = 0, className = '' }) {
  const { theme } = useChartTheme();
  const remaining = Math.max(100 - score, 0);
  const color = getScoreColorValue(score);

  const data = {
    labels: ['Score', 'Remaining'],
    datasets: [
      {
        data: [score, remaining],
        backgroundColor: [color, theme.grid],
        borderWidth: 0,
        cutout: '78%',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: { display: false },
      tooltip: { enabled: false },
    },
  };

  return (
    <div className={`relative mx-auto ${className}`} style={{ maxWidth: 220 }}>
      <Doughnut data={data} options={options} />
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-bold text-slate-800 dark:text-white">{Math.round(score)}</span>
        <span className="text-xs font-medium text-slate-500">{getScoreLabel(score)}</span>
      </div>
    </div>
  );
}
