export function Badge({ children, variant = 'default', className = '' }) {
  const variants = {
    default: 'bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-200',
    brand: 'bg-brand-100 text-brand-700 dark:bg-brand-900/50 dark:text-brand-300',
    success: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/50 dark:text-emerald-300',
    warning: 'bg-amber-100 text-amber-700 dark:bg-amber-900/50 dark:text-amber-300',
    danger: 'bg-red-100 text-red-700 dark:bg-red-900/50 dark:text-red-300',
    purple: 'bg-purple-100 text-purple-700 dark:bg-purple-900/50 dark:text-purple-300',
  };

  return (
    <span className={`inline-flex items-center rounded-lg px-2.5 py-0.5 text-xs font-medium ${variants[variant]} ${className}`}>
      {children}
    </span>
  );
}

export function SkillBadge({ skill, variant = 'brand' }) {
  return <Badge variant={variant}>{skill}</Badge>;
}
