export function LoadingSpinner({ size = 'md', text, fullScreen = false }) {
  const sizeClass = {
    sm: 'h-5 w-5 border-2',
    md: 'h-8 w-8 border-[3px]',
    lg: 'h-12 w-12 border-4',
  }[size];

  const spinner = (
    <div className="flex flex-col items-center gap-3">
      <div
        className={`${sizeClass} animate-spin rounded-full border-brand-200 border-t-brand-600 dark:border-slate-600 dark:border-t-brand-400`}
      />
      {text && <p className="text-sm font-medium text-slate-500 dark:text-slate-400">{text}</p>}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-white/80 backdrop-blur-sm dark:bg-slate-950/80">
        {spinner}
      </div>
    );
  }

  return spinner;
}

export function PageLoader({ text = 'Loading...' }) {
  return (
    <div className="flex min-h-[40vh] items-center justify-center">
      <LoadingSpinner size="lg" text={text} />
    </div>
  );
}

export function Skeleton({ className = '' }) {
  return (
    <div className={`animate-pulse rounded-lg bg-slate-200 dark:bg-slate-700 ${className}`} />
  );
}
