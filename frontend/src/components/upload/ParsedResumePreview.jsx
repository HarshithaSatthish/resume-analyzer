import { FiBookOpen, FiCode, FiMail, FiPhone, FiUser } from 'react-icons/fi';
import { Badge } from '../ui/Badge';
import { Card, CardHeader } from '../ui/Card';

function SectionBlock({ title, items, emptyText }) {
  if (!items?.length) {
    return (
      <div>
        <p className="mb-1 text-sm font-semibold text-slate-700 dark:text-slate-200">{title}</p>
        <p className="text-sm text-slate-500">{emptyText}</p>
      </div>
    );
  }

  return (
    <div>
      <p className="mb-2 text-sm font-semibold text-slate-700 dark:text-slate-200">{title}</p>
      <ul className="space-y-1.5">
        {items.map((item, index) => (
          <li key={index} className="rounded-lg bg-slate-50 px-3 py-2 text-sm dark:bg-slate-800/50">
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

export function ParsedResumePreview({ parsedData, metadata }) {
  if (!parsedData) return null;

  return (
    <Card glass className="animate-slide-up">
      <CardHeader
        title="Parsed Resume Preview"
        subtitle={
          metadata
            ? `${metadata.page_count} page(s) · ${metadata.extraction_method} · ${metadata.sections_found} sections detected`
            : 'Extracted resume information'
        }
      />

      <div className="mb-5 grid gap-3 sm:grid-cols-3">
        <div className="flex items-center gap-2 rounded-xl bg-slate-50 p-3 text-sm dark:bg-slate-800/50">
          <FiUser className="shrink-0 text-brand-500" />
          <span>{parsedData.name || 'Name not detected'}</span>
        </div>
        <div className="flex items-center gap-2 rounded-xl bg-slate-50 p-3 text-sm dark:bg-slate-800/50">
          <FiMail className="shrink-0 text-brand-500" />
          <span className="truncate">{parsedData.email || 'Email not detected'}</span>
        </div>
        <div className="flex items-center gap-2 rounded-xl bg-slate-50 p-3 text-sm dark:bg-slate-800/50">
          <FiPhone className="shrink-0 text-brand-500" />
          <span>{parsedData.phone || 'Phone not detected'}</span>
        </div>
      </div>

      {parsedData.summary && (
        <div className="mb-5 rounded-xl border border-brand-100 bg-brand-50/50 p-4 dark:border-brand-900 dark:bg-brand-950/20">
          <p className="text-xs font-semibold uppercase tracking-wide text-brand-600">Summary</p>
          <p className="mt-1 text-sm text-slate-700 dark:text-slate-200">{parsedData.summary}</p>
        </div>
      )}

      {parsedData.skills?.length > 0 && (
        <div className="mb-5">
          <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-slate-700 dark:text-slate-200">
            <FiCode className="text-brand-500" /> Skills ({parsedData.skills.length})
          </div>
          <div className="flex flex-wrap gap-1.5">
            {parsedData.skills.map((skill) => (
              <Badge key={skill} variant="brand">{skill}</Badge>
            ))}
          </div>
        </div>
      )}

      <div className="grid gap-5 lg:grid-cols-2">
        <SectionBlock title="Experience" items={parsedData.experience} emptyText="No experience section detected" />
        <SectionBlock title="Education" items={parsedData.education} emptyText="No education section detected" />
        <SectionBlock title="Projects" items={parsedData.projects} emptyText="No projects section detected" />
        <SectionBlock title="Certifications" items={parsedData.certifications} emptyText="No certifications detected" />
      </div>

      {parsedData.languages?.length > 0 && (
        <div className="mt-5">
          <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-slate-700 dark:text-slate-200">
            <FiBookOpen className="text-brand-500" /> Languages
          </div>
          <div className="flex flex-wrap gap-1.5">
            {parsedData.languages.map((lang) => (
              <Badge key={lang} variant="purple">{lang}</Badge>
            ))}
          </div>
        </div>
      )}
    </Card>
  );
}
