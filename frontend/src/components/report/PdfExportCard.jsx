import { FiCheckCircle, FiFileText } from 'react-icons/fi';
import { Card, CardHeader } from '../ui/Card';
import { DownloadPdfButton } from './DownloadPdfButton';

const PDF_SECTIONS = [
  'Candidate contact details',
  'ATS score breakdown with chart',
  'Grade and recommendations',
  'Parsed resume sections',
  'Detected skills',
  'Gemini AI feedback',
  'Job comparison results (if available)',
];

export function PdfExportCard({ reportId, title, pdfAvailable }) {
  return (
    <Card glass>
      <CardHeader
        title="PDF Export"
        subtitle={pdfAvailable ? 'Professional report ready to download' : 'PDF will be generated on download'}
        action={<DownloadPdfButton reportId={reportId} title={title} showLabel={false} iconOnly={false} />}
      />
      <div className="flex items-start gap-4">
        <div className="rounded-xl bg-brand-50 p-3 text-brand-600 dark:bg-brand-950/40 dark:text-brand-400">
          <FiFileText className="h-6 w-6" />
        </div>
        <ul className="space-y-1.5 text-sm text-slate-600 dark:text-slate-300">
          {PDF_SECTIONS.map((section) => (
            <li key={section} className="flex items-start gap-2">
              <FiCheckCircle className="mt-0.5 shrink-0 text-emerald-500" />
              <span>{section}</span>
            </li>
          ))}
        </ul>
      </div>
    </Card>
  );
}
