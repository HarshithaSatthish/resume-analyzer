import { Doughnut } from 'react-chartjs-2';
import { useChartTheme } from '../../hooks/useChartTheme';
import { CHART_PALETTE } from '../../utils/chartTheme';
import { Badge } from '../ui/Badge';
import { ChartEmptyState } from './ChartCard';
import './chartRegistry';

export function SkillDistributionChart({ skills = [], maxDisplay = 10, className = '', showBadges = true }) {
  const { theme, baseOptions } = useChartTheme();

  if (!skills.length) {
    return <ChartEmptyState message="No skills detected" className={className} />;
  }

  const displaySkills = skills.slice(0, maxDisplay);
  const otherCount = Math.max(skills.length - maxDisplay, 0);

  const labels = [...displaySkills];
  const values = displaySkills.map(() => 1);

  if (otherCount > 0) {
    labels.push(`+${otherCount} more`);
    values.push(otherCount);
  }

  const data = {
    labels,
    datasets: [
      {
        data: values,
        backgroundColor: CHART_PALETTE.slice(0, labels.length),
        borderWidth: 2,
        borderColor: theme.border,
      },
    ],
  };

  const options = baseOptions({
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (ctx) => ` ${ctx.label}`,
        },
      },
    },
  });

  return (
    <div className={className}>
      <div className="h-56">
        <Doughnut data={data} options={options} />
      </div>
      {showBadges && (
        <div className="mt-4 flex flex-wrap gap-1.5">
          {displaySkills.map((skill) => (
            <Badge key={skill} variant="brand">{skill}</Badge>
          ))}
          {otherCount > 0 && <Badge variant="default">+{otherCount} more</Badge>}
        </div>
      )}
    </div>
  );
}
