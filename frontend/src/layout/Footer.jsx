export function Footer() {
  return (
    <footer className="border-t border-slate-200/80 bg-white/50 px-4 py-4 dark:border-slate-700/50 dark:bg-slate-900/50">
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-2 sm:flex-row">
        <p className="text-xs text-slate-500 dark:text-slate-400">
          © {new Date().getFullYear()} AI Resume Analyzer. All rights reserved.
        </p>
        <p className="text-xs text-slate-400">
          Powered by Gemini AI · ATS Scoring · spaCy NLP
        </p>
      </div>
    </footer>
  );
}
