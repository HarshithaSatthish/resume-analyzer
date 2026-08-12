import { FiAward, FiBookOpen, FiBriefcase, FiCpu, FiTarget, FiTrendingUp } from 'react-icons/fi';
import { Badge } from '../ui/Badge';
import { Card, CardHeader } from '../ui/Card';

function ListSection({ title, icon: Icon, items, variant = 'brand', emptyText }) {
  return (
    <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
      <div className="mb-3 flex items-center gap-2">
        <Icon className="h-4 w-4 text-brand-500" />
        <h4 className="text-sm font-semibold text-slate-800 dark:text-white">{title}</h4>
      </div>
      {items?.length ? (
        <ul className="space-y-2">
          {items.map((item, index) => (
            <li key={index} className="flex gap-2 text-sm text-slate-600 dark:text-slate-300">
              <Badge variant={variant}>{index + 1}</Badge>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-slate-500">{emptyText}</p>
      )}
    </div>
  );
}

export function AIFeedbackPanel({ feedback, compact = false }) {
  if (!feedback) return null;

  const isGemini = feedback.source === 'gemini';

  return (
    <div className={compact ? 'space-y-4' : 'space-y-6'}>
      <div className="flex flex-wrap items-center gap-2">
        <Badge variant={isGemini ? 'success' : 'warning'}>
          {isGemini ? 'Powered by Gemini AI' : 'Rule-based fallback'}
        </Badge>
        {feedback.model && (
          <Badge variant="default">{feedback.model}</Badge>
        )}
      </div>

      <Card glass className="!p-4">
        <CardHeader title="Resume Feedback" />
        <p className="text-sm leading-relaxed text-slate-600 dark:text-slate-300">
          {feedback.resume_feedback}
        </p>
      </Card>

      {feedback.professional_summary && (
        <div className="rounded-xl border border-brand-100 bg-gradient-to-r from-brand-50 to-accent-50 p-4 dark:border-brand-900 dark:from-brand-950/30 dark:to-accent-950/20">
          <p className="text-xs font-semibold uppercase tracking-wide text-brand-600">Professional Summary</p>
          <p className="mt-2 text-sm leading-relaxed text-slate-700 dark:text-slate-200">
            {feedback.professional_summary}
          </p>
        </div>
      )}

      <div className="grid gap-4 lg:grid-cols-2">
        <ListSection title="Strengths" icon={FiTrendingUp} items={feedback.strengths} variant="success" emptyText="No strengths identified" />
        <ListSection title="Weaknesses" icon={FiTarget} items={feedback.weaknesses} variant="warning" emptyText="No weaknesses identified" />
        <ListSection title="Resume Improvements" icon={FiBriefcase} items={feedback.resume_improvements} emptyText="No improvements suggested" />
        <ListSection title="Career Suggestions" icon={FiAward} items={feedback.career_suggestions} emptyText="No career suggestions" />
        <ListSection title="Recommended Certifications" icon={FiBookOpen} items={feedback.recommended_certifications} variant="purple" emptyText="No certifications suggested" />
        <ListSection title="Recommended Projects" icon={FiCpu} items={feedback.recommended_projects} variant="brand" emptyText="No projects suggested" />
      </div>
    </div>
  );
}
