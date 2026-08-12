import { FiAlertCircle, FiAward } from 'react-icons/fi';
import { SCORE_METRICS } from '../../utils/chartTheme';
import { getScoreColor } from '../../utils/formatters';
import { ATSGaugeChart } from './ATSGaugeChart';
import { Badge } from '../ui/Badge';
import { Card, CardHeader } from '../ui/Card';
import { ProgressBar } from '../ui/ProgressBar';

export function ATSBreakdownPanel({ scores, compact = false }) {
  if (!scores) return null;

  return (
    <div className={compact ? 'space-y-4' : 'space-y-6'}>
      <div className="flex flex-wrap items-center justify-center gap-6">
        <ATSGaugeChart score={scores.overall_score} />
        {scores.grade && (
          <div className="text-center">
            <div className="flex items-center justify-center gap-2">
              <FiAward className="h-6 w-6 text-amber-500" />
              <span className={`text-4xl font-bold ${getScoreColor(scores.overall_score)}`}>
                {scores.grade}
              </span>
            </div>
            <p className="mt-1 text-sm text-slate-500">ATS Grade</p>
          </div>
        )}
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        {SCORE_METRICS.map(({ key, label, weight }) => (
          <ProgressBar
            key={key}
            label={`${label} (${weight})`}
            value={scores[key]}
            size="sm"
          />
        ))}
      </div>

      {scores.recommendations?.length > 0 && (
        <Card glass className="!p-4">
          <CardHeader title="ATS Recommendations" subtitle="Improve your resume compatibility" />
          <ul className="space-y-2">
            {scores.recommendations.map((item, index) => (
              <li key={index} className="flex gap-2 text-sm text-slate-600 dark:text-slate-300">
                <FiAlertCircle className="mt-0.5 shrink-0 text-brand-500" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
}

export function ATSGradeBadge({ grade, score }) {
  if (!grade) return null;
  const variant = score >= 80 ? 'success' : score >= 60 ? 'brand' : score >= 40 ? 'warning' : 'danger';
  return <Badge variant={variant}>Grade {grade}</Badge>;
}
