import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { FiArrowRight, FiFileText, FiTrendingUp, FiUpload } from 'react-icons/fi';
import { Card, CardHeader, StatCard } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { PageLoader } from '../components/ui/LoadingSpinner';
import { ProgressBar } from '../components/ui/ProgressBar';
import { getHistory } from '../services/reportService';
import { getErrorMessage } from '../services/api';
import { useToast } from '../context/ToastContext';
import { DashboardChartsSection } from '../components/charts';
import { formatDate, formatScore, getScoreColor } from '../utils/formatters';

export default function Dashboard() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const toast = useToast();

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await getHistory();
        setReports(data.reports || []);
      } catch (error) {
        toast.error(getErrorMessage(error));
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, [toast]);

  if (loading) return <PageLoader text="Loading dashboard..." />;

  const totalReports = reports.length;
  const avgScore = totalReports
    ? Math.round(reports.reduce((sum, r) => sum + r.overall_score, 0) / totalReports)
    : 0;
  const highestScore = totalReports ? Math.max(...reports.map((r) => r.overall_score)) : 0;
  const recentReports = reports.slice(0, 5);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 dark:text-white">
            Dashboard <span className="gradient-text">Overview</span>
          </h2>
          <p className="mt-1 text-sm text-slate-500">Track your resume analysis performance</p>
        </div>
        <Link to="/analyze">
          <Button>
            <FiUpload className="h-4 w-4" />
            Upload Resume
          </Button>
        </Link>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Total Reports" value={totalReports} icon={FiFileText} color="brand" />
        <StatCard label="Average ATS Score" value={`${avgScore}%`} icon={FiTrendingUp} color="green" trend="Across all analyses" />
        <StatCard label="Best Score" value={`${Math.round(highestScore)}%`} icon={FiTrendingUp} color="purple" />
        <StatCard label="Recent Activity" value={recentReports.length} icon={FiFileText} color="amber" trend="Last 5 reports" />
      </div>

      {totalReports > 0 && <DashboardChartsSection reports={reports} />}

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2" glass>
          <CardHeader
            title="Recent Reports"
            subtitle="Your latest resume analyses"
            action={
              <Link to="/history" className="text-sm font-medium text-brand-600 hover:text-brand-700 dark:text-brand-400">
                View all
              </Link>
            }
          />

          {recentReports.length === 0 ? (
            <div className="flex flex-col items-center py-12 text-center">
              <div className="mb-4 rounded-2xl bg-brand-50 p-4 dark:bg-brand-950/30">
                <FiUpload className="h-8 w-8 text-brand-500" />
              </div>
              <p className="font-medium text-slate-600 dark:text-slate-300">No reports yet</p>
              <p className="mt-1 text-sm text-slate-500">Upload your first resume to get started</p>
              <Link to="/analyze" className="mt-4">
                <Button>Analyze Resume</Button>
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {recentReports.map((report) => (
                <Link
                  key={report.id}
                  to={`/report/${report.id}`}
                  className="flex items-center justify-between rounded-xl border border-slate-100 p-4 transition-all hover:border-brand-200 hover:bg-brand-50/50 dark:border-slate-700 dark:hover:border-brand-700 dark:hover:bg-brand-950/20"
                >
                  <div className="min-w-0 flex-1">
                    <p className="truncate font-semibold text-slate-800 dark:text-white">{report.title}</p>
                    <p className="text-xs text-slate-500">{formatDate(report.created_at)}</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`text-lg font-bold ${getScoreColor(report.overall_score)}`}>
                      {formatScore(report.overall_score)}%
                    </span>
                    <FiArrowRight className="text-slate-400" />
                  </div>
                </Link>
              ))}
            </div>
          )}
        </Card>

        <Card glass>
          <CardHeader title="Quick Actions" subtitle="Get started quickly" />
          <div className="space-y-3">
            <Link to="/analyze" className="block">
              <div className="rounded-xl bg-gradient-to-r from-brand-500 to-accent-500 p-4 text-white transition-transform hover:scale-[1.02]">
                <FiUpload className="mb-2 h-6 w-6" />
                <p className="font-semibold">Upload & Analyze</p>
                <p className="text-xs text-brand-100">Get ATS score instantly</p>
              </div>
            </Link>
            <Link to="/history" className="block">
              <div className="rounded-xl border border-slate-200 p-4 transition-all hover:border-brand-300 dark:border-slate-600">
                <FiFileText className="mb-2 h-6 w-6 text-brand-500" />
                <p className="font-semibold text-slate-800 dark:text-white">View History</p>
                <p className="text-xs text-slate-500">Browse past reports</p>
              </div>
            </Link>
          </div>

          {totalReports > 0 && (
            <div className="mt-6">
              <p className="mb-2 text-sm font-medium text-slate-600 dark:text-slate-300">Score Distribution</p>
              <ProgressBar value={avgScore} label="Average ATS" size="lg" />
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
