import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import {
  FiArrowLeft,
  FiMail,
  FiPhone,
  FiTrash2,
  FiUser,
} from 'react-icons/fi';
import { DownloadPdfButton } from '../components/report/DownloadPdfButton';
import { PdfExportCard } from '../components/report/PdfExportCard';
import { AIFeedbackPanel } from '../components/ai/AIFeedbackPanel';
import { ATSBreakdownPanel, ATSGradeBadge, JobMatchChart, ReportChartsGrid } from '../components/charts';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Card, CardHeader } from '../components/ui/Card';
import { PageLoader } from '../components/ui/LoadingSpinner';
import { ProgressBar } from '../components/ui/ProgressBar';
import { Textarea } from '../components/ui/Input';
import { useToast } from '../context/ToastContext';
import { getReport, deleteReport } from '../services/reportService';
import { compareJobDescription } from '../services/resumeService';
import { getErrorMessage } from '../services/api';
import { formatDate } from '../utils/formatters';

export default function Report() {
  const { id } = useParams();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [jobDescription, setJobDescription] = useState('');
  const [comparing, setComparing] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const toast = useToast();

  const fetchReport = async () => {
    try {
      const data = await getReport(id);
      setReport(data);
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReport();
  }, [id]);

  const handleCompare = async () => {
    if (jobDescription.trim().length < 20) {
      toast.error('Job description must be at least 20 characters.');
      return;
    }

    setComparing(true);
    try {
      await compareJobDescription(id, jobDescription);
      toast.success('Job comparison complete!');
      await fetchReport();
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setComparing(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this report?')) return;
    setDeleting(true);
    try {
      await deleteReport(id);
      toast.success('Report deleted.');
      window.location.href = '/history';
    } catch (error) {
      toast.error(getErrorMessage(error));
      setDeleting(false);
    }
  };

  if (loading) return <PageLoader text="Loading report..." />;
  if (!report) {
    return (
      <div className="py-20 text-center">
        <p className="text-slate-500">Report not found.</p>
        <Link to="/history" className="mt-4 inline-block text-brand-600">Back to history</Link>
      </div>
    );
  }

  const { parsed_data: parsed, ats_scores: scores, ai_feedback: ai, job_comparison: comparison } = report;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Link to="/history" className="rounded-lg p-2 text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800">
            <FiArrowLeft className="h-5 w-5" />
          </Link>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-2xl font-bold text-slate-800 dark:text-white">{report.title}</h2>
              <ATSGradeBadge grade={scores.grade} score={scores.overall_score} />
            </div>
            <p className="text-sm text-slate-500">{formatDate(report.created_at)}</p>
          </div>
        </div>
        <div className="flex gap-2">
          <DownloadPdfButton reportId={id} title={report.title} />
          <Button variant="secondary" onClick={handleDelete} loading={deleting} className="!text-red-500">
            <FiTrash2 className="h-4 w-4" /> Delete
          </Button>
        </div>
      </div>

      <Card glass>
        <CardHeader title="ATS Score Analysis" subtitle="Weighted compatibility scoring across 7 dimensions" />
        <ATSBreakdownPanel scores={scores} />
      </Card>

      <ReportChartsGrid scores={scores} skills={report.detected_skills} />

      <PdfExportCard reportId={id} title={report.title} pdfAvailable={report.pdf_available} />

      <div className="grid gap-6 lg:grid-cols-3">
        <Card glass>
          <CardHeader title="Contact Info" />
          <div className="space-y-3">
            <div className="flex items-center gap-3 text-sm">
              <FiUser className="text-brand-500" />
              <span>{parsed.name || 'Not detected'}</span>
            </div>
            <div className="flex items-center gap-3 text-sm">
              <FiMail className="text-brand-500" />
              <span>{parsed.email || 'Not detected'}</span>
            </div>
            <div className="flex items-center gap-3 text-sm">
              <FiPhone className="text-brand-500" />
              <span>{parsed.phone || 'Not detected'}</span>
            </div>
          </div>
        </Card>

        {parsed.summary && (
          <Card glass className="lg:col-span-2">
            <CardHeader title="Professional Summary" />
            <p className="text-sm leading-relaxed text-slate-600 dark:text-slate-300">{parsed.summary}</p>
          </Card>
        )}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {[
          { title: 'Education', items: parsed.education },
          { title: 'Experience', items: parsed.experience },
          { title: 'Projects', items: parsed.projects },
          { title: 'Certifications', items: parsed.certifications },
        ].map(({ title, items }) => (
          <Card key={title} glass>
            <CardHeader title={title} />
            {items?.length ? (
              <ul className="space-y-2">
                {items.map((item, i) => (
                  <li key={i} className="rounded-lg bg-slate-50 px-3 py-2 text-sm dark:bg-slate-800/50">
                    {item}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-slate-500">No {title.toLowerCase()} detected</p>
            )}
          </Card>
        ))}
      </div>

      <Card glass>
        <CardHeader title="Gemini AI Insights" subtitle="Career coaching and resume improvement recommendations" />
        <AIFeedbackPanel feedback={ai} />
      </Card>

      <Card glass>
        <CardHeader title="Job Description Comparison" subtitle="Paste a job description to find skill gaps" />
        <Textarea
          placeholder="Paste the job description here (minimum 20 characters)..."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          rows={5}
        />
        <div className="mt-4">
          <Button onClick={handleCompare} loading={comparing} disabled={jobDescription.trim().length < 20}>
            Compare with Resume
          </Button>
        </div>

        {comparison && (
          <div className="mt-6 space-y-4 rounded-xl border border-slate-200 p-4 dark:border-slate-700">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-700 dark:text-slate-200">Match Percentage</span>
              <span className="text-2xl font-bold text-brand-600">{Math.round(comparison.match_percentage)}%</span>
            </div>
            <ProgressBar value={comparison.match_percentage} size="lg" showValue={false} />
            <JobMatchChart comparison={comparison} />
            <div>
              <p className="mb-2 text-sm font-semibold text-emerald-600">Matched Skills</p>
              <div className="flex flex-wrap gap-1.5">
                {comparison.matched_skills?.length
                  ? comparison.matched_skills.map((s) => <Badge key={s} variant="success">{s}</Badge>)
                  : <span className="text-sm text-slate-500">None</span>}
              </div>
            </div>
            <div>
              <p className="mb-2 text-sm font-semibold text-red-500">Missing Skills</p>
              <div className="flex flex-wrap gap-1.5">
                {comparison.missing_skills?.length
                  ? comparison.missing_skills.map((s) => <Badge key={s} variant="danger">{s}</Badge>)
                  : <span className="text-sm text-slate-500">None — great match!</span>}
              </div>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
