import { ATSGaugeChart } from './ATSGaugeChart';
import { ScoreBarChart } from './ScoreBarChart';
import { ScoreDistributionChart } from './ScoreDistributionChart';
import { ScorePieChart } from './ScorePieChart';
import { ScoreTrendChart } from './ScoreTrendChart';
import { SkillDistributionChart } from './SkillDistributionChart';
import { ChartCard } from './ChartCard';

export function ReportChartsGrid({ scores, skills }) {
  return (
    <div className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-2">
        <ChartCard title="ATS Bar Chart" subtitle="Score by dimension">
          <ScoreBarChart scores={scores} />
        </ChartCard>
        <ChartCard title="ATS Pie Chart" subtitle="Proportional score distribution">
          <ScorePieChart scores={scores} />
        </ChartCard>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <ChartCard title="ATS Gauge" subtitle="Overall compatibility" className="flex flex-col items-center">
          <div className="py-4">
            <ATSGaugeChart score={scores?.overall_score || 0} />
          </div>
        </ChartCard>
        <ChartCard title="Skill Distribution" subtitle={`${skills?.length || 0} skills detected`} className="lg:col-span-2">
          <SkillDistributionChart skills={skills || []} />
        </ChartCard>
      </div>
    </div>
  );
}

export function DashboardChartsSection({ reports }) {
  if (!reports.length) return null;

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <ChartCard title="Score Trend" subtitle="ATS scores over time">
        <ScoreTrendChart reports={reports} />
      </ChartCard>
      <ChartCard title="Score Distribution" subtitle="Reports grouped by score range">
        <ScoreDistributionChart reports={reports} />
      </ChartCard>
    </div>
  );
}
