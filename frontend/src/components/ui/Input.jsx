export function Input({
  label,
  error,
  id,
  className = '',
  containerClassName = '',
  ...props
}) {
  const inputId = id || props.name;

  return (
    <div className={`space-y-1.5 ${containerClassName}`}>
      {label && (
        <label htmlFor={inputId} className="block text-sm font-medium text-slate-700 dark:text-slate-300">
          {label}
        </label>
      )}
      <input id={inputId} className={`input-field ${error ? 'border-red-400 focus:border-red-500 focus:ring-red-500/20' : ''} ${className}`} {...props} />
      {error && <p className="text-xs text-red-500">{error}</p>}
    </div>
  );
}

export function Textarea({
  label,
  error,
  id,
  className = '',
  containerClassName = '',
  rows = 4,
  ...props
}) {
  const inputId = id || props.name;

  return (
    <div className={`space-y-1.5 ${containerClassName}`}>
      {label && (
        <label htmlFor={inputId} className="block text-sm font-medium text-slate-700 dark:text-slate-300">
          {label}
        </label>
      )}
      <textarea
        id={inputId}
        rows={rows}
        className={`input-field resize-y ${error ? 'border-red-400 focus:border-red-500 focus:ring-red-500/20' : ''} ${className}`}
        {...props}
      />
      {error && <p className="text-xs text-red-500">{error}</p>}
    </div>
  );
}
