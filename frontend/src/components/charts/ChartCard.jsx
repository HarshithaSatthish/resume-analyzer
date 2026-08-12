import { Card, CardHeader } from '../ui/Card';

export function ChartCard({ title, subtitle, children, className = '', action }) {
  return (
    <Card glass className={className}>
      {(title || subtitle) && (
        <CardHeader title={title} subtitle={subtitle} action={action} />
      )}
      {children}
    </Card>
  );
}

export function ChartEmptyState({ message = 'No chart data available', className = '' }) {
  return (
    <div className={`flex h-48 items-center justify-center rounded-xl border border-dashed border-slate-200 text-sm text-slate-500 dark:border-slate-700 ${className}`}>
      {message}
    </div>
  );
}
