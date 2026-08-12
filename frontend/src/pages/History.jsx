import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { FiArrowRight, FiSearch, FiTrash2 } from 'react-icons/fi';
import { DownloadPdfButton } from '../components/report/DownloadPdfButton';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { PageLoader } from '../components/ui/LoadingSpinner';
import { useDebounce } from '../hooks/useDebounce';
import { useToast } from '../context/ToastContext';
import { getHistory, deleteReport } from '../services/reportService';
import { getErrorMessage } from '../services/api';
import { formatDate, formatScore, getScoreColor } from '../utils/formatters';

export default function History() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [deletingId, setDeletingId] = useState(null);
  const debouncedSearch = useDebounce(search);
  const toast = useToast();

  const fetchHistory = async (query = '') => {
    setLoading(true);
    try {
      const data = await getHistory(query);
      setReports(data.reports || []);
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory(debouncedSearch);
  }, [debouncedSearch]);

  const handleDelete = async (reportId, event) => {
    event.preventDefault();
    event.stopPropagation();
    if (!window.confirm('Delete this report permanently?')) return;

    setDeletingId(reportId);
    try {
      await deleteReport(reportId);
      setReports((prev) => prev.filter((r) => r.id !== reportId));
      toast.success('Report deleted.');
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 dark:text-white">
            Report <span className="gradient-text">History</span>
          </h2>
          <p className="mt-1 text-sm text-slate-500">{reports.length} report{reports.length !== 1 ? 's' : ''} found</p>
        </div>
      </div>

      <div className="relative max-w-md">
        <FiSearch className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
        <Input
          placeholder="Search reports..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="pl-10"
        />
      </div>

      {loading ? (
        <PageLoader text="Loading reports..." />
      ) : reports.length === 0 ? (
        <Card glass className="py-16 text-center">
          <p className="text-slate-500">
            {search ? 'No reports match your search.' : 'No reports yet. Analyze your first resume!'}
          </p>
          {!search && (
            <Link to="/analyze" className="mt-4 inline-block">
              <Button>Analyze Resume</Button>
            </Link>
          )}
        </Card>
      ) : (
        <div className="space-y-3">
          {reports.map((report) => (
            <Link key={report.id} to={`/report/${report.id}`}>
              <Card hover className="flex items-center justify-between gap-4 !p-4">
                <div className="min-w-0 flex-1">
                  <p className="truncate font-semibold text-slate-800 dark:text-white">{report.title}</p>
                  <p className="text-xs text-slate-500">{formatDate(report.created_at)}</p>
                </div>

                <div className="flex items-center gap-3">
                  <span className={`text-xl font-bold ${getScoreColor(report.overall_score)}`}>
                    {formatScore(report.overall_score)}%
                  </span>

                  <DownloadPdfButton
                    reportId={report.id}
                    title={report.title}
                    iconOnly
                  />

                  <button
                    type="button"
                    onClick={(e) => handleDelete(report.id, e)}
                    disabled={deletingId === report.id}
                    className="rounded-lg p-2 text-slate-400 transition-colors hover:bg-red-50 hover:text-red-500 dark:hover:bg-red-950/30"
                    aria-label="Delete report"
                  >
                    <FiTrash2 className="h-4 w-4" />
                  </button>

                  <FiArrowRight className="hidden text-slate-400 sm:block" />
                </div>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
