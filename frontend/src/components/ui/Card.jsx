export function Card({ children, className = '', hover = false, glass = false }) {
  const base = glass ? 'glass-card' : 'glass-card-solid';
  const hoverClass = hover ? 'transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg' : '';

  return (
    <div className={`${base} p-5 sm:p-6 ${hoverClass} ${className}`}>
      {children}
    </div>
  );
}

export function CardHeader({ title, subtitle, action, className = '' }) {
  return (
    <div className={`mb-4 flex flex-wrap items-start justify-between gap-3 ${className}`}>
      <div>
        {title && <h3 className="text-lg font-semibold text-slate-800 dark:text-slate-100">{title}</h3>}
        {subtitle && <p className="mt-0.5 text-sm text-slate-500 dark:text-slate-400">{subtitle}</p>}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}

export function StatCard({ label, value, icon: Icon, trend, color = 'brand' }) {
  const colorMap = {
    brand: 'from-brand-500 to-accent-500',
    green: 'from-emerald-500 to-teal-500',
    amber: 'from-amber-500 to-orange-500',
    purple: 'from-purple-500 to-pink-500',
  };

  return (
    <Card hover className="relative overflow-hidden">
      <div className={`absolute -right-4 -top-4 h-24 w-24 rounded-full bg-gradient-to-br ${colorMap[color]} opacity-10`} />
      <div className="relative flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500 dark:text-slate-400">{label}</p>
          <p className="mt-1 text-3xl font-bold text-slate-800 dark:text-white">{value}</p>
          {trend && <p className="mt-1 text-xs text-slate-400">{trend}</p>}
        </div>
        {Icon && (
          <div className={`rounded-xl bg-gradient-to-br ${colorMap[color]} p-2.5 text-white shadow-md`}>
            <Icon className="h-5 w-5" />
          </div>
        )}
      </div>
    </Card>
  );
}
