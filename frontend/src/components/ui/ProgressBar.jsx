import { getScoreBgColor } from '../../utils/formatters';

export function ProgressBar({ value = 0, max = 100, label, showValue = true, size = 'md', className = '' }) {
  const percent = Math.min(Math.max((value / max) * 100, 0), 100);
  const height = size === 'sm' ? 'h-1.5' : size === 'lg' ? 'h-3' : 'h-2';

  return (
    <div className={className}>
      {(label || showValue) && (
        <div className="mb-1.5 flex items-center justify-between text-sm">
          {label && <span className="font-medium text-slate-600 dark:text-slate-300">{label}</span>}
          {showValue && <span className="font-semibold text-slate-700 dark:text-slate-200">{Math.round(percent)}%</span>}
        </div>
      )}
      <div className={`w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700 ${height}`}>
        <div
          className={`${height} rounded-full transition-all duration-500 ease-out ${getScoreBgColor(percent)}`}
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}

export function CircularProgress({ value = 0, size = 120, strokeWidth = 10, label }) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;

  const color =
    value >= 80 ? '#10b981' : value >= 60 ? '#6366f1' : value >= 40 ? '#f59e0b' : '#ef4444';

  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          className="text-slate-200 dark:text-slate-700"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="transition-all duration-700 ease-out"
        />
      </svg>
      <div className="absolute text-center">
        <span className="text-2xl font-bold text-slate-800 dark:text-white">{Math.round(value)}</span>
        {label && <p className="text-xs text-slate-500">{label}</p>}
      </div>
    </div>
  );
}
