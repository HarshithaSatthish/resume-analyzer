import { FiDownload } from 'react-icons/fi';
import { useState } from 'react';
import { Button } from '../ui/Button';
import { useToast } from '../../context/ToastContext';
import { downloadReport } from '../../services/reportService';
import { getErrorMessage } from '../../services/api';

export function DownloadPdfButton({
  reportId,
  title = 'resume-report',
  variant = 'secondary',
  size = 'md',
  className = '',
  showLabel = true,
  iconOnly = false,
  onSuccess,
}) {
  const [downloading, setDownloading] = useState(false);
  const toast = useToast();

  const handleDownload = async (event) => {
    event?.preventDefault?.();
    event?.stopPropagation?.();

    setDownloading(true);
    try {
      const filename = `${title.replace(/\s+/g, '_')}.pdf`;
      await downloadReport(reportId, filename);
      toast.success('PDF report downloaded!');
      onSuccess?.();
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setDownloading(false);
    }
  };

  if (iconOnly) {
    return (
      <button
        type="button"
        onClick={handleDownload}
        disabled={downloading}
        className={`rounded-lg p-2 text-slate-400 transition-colors hover:bg-brand-50 hover:text-brand-600 disabled:cursor-not-allowed disabled:opacity-50 dark:hover:bg-brand-950/30 ${className}`}
        aria-label="Download PDF report"
      >
        <FiDownload className={`h-4 w-4 ${downloading ? 'animate-pulse' : ''}`} />
      </button>
    );
  }

  return (
    <Button variant={variant} size={size} onClick={handleDownload} loading={downloading} className={className}>
      <FiDownload className="h-4 w-4" />
      {showLabel && (downloading ? 'Downloading...' : 'Download PDF')}
    </Button>
  );
}
