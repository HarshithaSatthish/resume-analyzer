import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiCpu, FiEye, FiFile, FiZap } from 'react-icons/fi';
import { ResumeDropzone } from '../components/upload/ResumeDropzone';
import { ParsedResumePreview } from '../components/upload/ParsedResumePreview';
import { ATSBreakdownPanel } from '../components/charts/ATSBreakdownPanel';
import { AIFeedbackPanel } from '../components/ai/AIFeedbackPanel';
import { Button } from '../components/ui/Button';
import { Card, CardHeader } from '../components/ui/Card';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { useToast } from '../context/ToastContext';
import { uploadResume, parseResume, calculateATSScore, generateAIFeedback, analyzeResume } from '../services/resumeService';
import { getErrorMessage } from '../services/api';

export default function Analyze() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [isParsing, setIsParsing] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [parseResult, setParseResult] = useState(null);
  const [atsResult, setAtsResult] = useState(null);
  const [aiResult, setAiResult] = useState(null);
  const [isScoring, setIsScoring] = useState(false);
  const [isGeneratingAI, setIsGeneratingAI] = useState(false);
  const toast = useToast();
  const navigate = useNavigate();

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setUploadedFile(null);
    setParseResult(null);
    setAtsResult(null);
    setAiResult(null);
  };

  const handleUploadAndParse = async () => {
    if (!selectedFile) {
      toast.error('Please select a PDF resume first.');
      return;
    }

    setIsUploading(true);
    setUploadProgress(0);
    setParseResult(null);
    setAtsResult(null);
    setAiResult(null);

    try {
      const uploadResult = await uploadResume(selectedFile, setUploadProgress);
      setUploadedFile(uploadResult);
      toast.success('Resume uploaded successfully!');

      setIsUploading(false);
      setIsParsing(true);

      const parsed = await parseResume(uploadResult.file_id);
      setParseResult(parsed);
      toast.success('Resume parsed successfully!');

      setIsScoring(true);
      const ats = await calculateATSScore(uploadResult.file_id);
      setAtsResult(ats);

      setIsScoring(false);
      setIsGeneratingAI(true);
      const ai = await generateAIFeedback(uploadResult.file_id);
      setAiResult(ai);
    } catch (error) {
      toast.error(getErrorMessage(error));
      setSelectedFile(null);
      setUploadedFile(null);
    } finally {
      setIsUploading(false);
      setIsParsing(false);
      setIsScoring(false);
      setIsGeneratingAI(false);
    }
  };

  const handleAnalyze = async () => {
    if (!uploadedFile?.file_id) {
      toast.error('Upload and parse a resume first.');
      return;
    }

    setIsAnalyzing(true);
    try {
      const analysisResult = await analyzeResume(uploadedFile.file_id);
      toast.success('Analysis complete!');
      navigate(`/report/${analysisResult.report_id}`);
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setIsAnalyzing(false);
    }
  };

  const isProcessing = isUploading || isParsing || isScoring || isGeneratingAI || isAnalyzing;

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-slate-800 dark:text-white">
          Analyze Your <span className="gradient-text">Resume</span>
        </h2>
        <p className="mt-1 text-sm text-slate-500">
          Upload a PDF, preview extracted data, then run full ATS and AI analysis
        </p>
      </div>

      <Card glass>
        <CardHeader
          title="Upload Resume"
          subtitle="Only resume or CV PDFs are accepted — other documents are rejected"
        />
        <ResumeDropzone
          selectedFile={selectedFile}
          onFileSelect={handleFileSelect}
          disabled={isProcessing}
          uploadProgress={uploadProgress}
          isUploading={isUploading}
        />

        {uploadedFile && !isUploading && (
          <div className="mt-4 flex items-center gap-3 rounded-xl bg-emerald-50 p-3 dark:bg-emerald-950/30">
            <FiFile className="h-5 w-5 text-emerald-500" />
            <p className="text-sm text-emerald-700 dark:text-emerald-300">
              Uploaded: {uploadedFile.original_filename}
            </p>
          </div>
        )}

        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <Button
            onClick={handleUploadAndParse}
            loading={isUploading || isParsing || isScoring || isGeneratingAI}
            disabled={!selectedFile || isProcessing}
            variant="secondary"
          >
            {isUploading ? (
              'Uploading...'
            ) : isParsing ? (
              <>
                <FiEye className="h-4 w-4" />
                Parsing...
              </>
            ) : isScoring ? (
              <>
                <FiEye className="h-4 w-4" />
                Scoring ATS...
              </>
            ) : isGeneratingAI ? (
              <>
                <FiEye className="h-4 w-4" />
                Generating AI...
              </>
            ) : (
              <>
                <FiEye className="h-4 w-4" />
                Upload & Parse
              </>
            )}
          </Button>

          <Button
            onClick={handleAnalyze}
            loading={isAnalyzing}
            disabled={!parseResult || isProcessing}
            className="min-w-[180px]"
          >
            {isAnalyzing ? (
              <>
                <FiCpu className="h-4 w-4" />
                Analyzing...
              </>
            ) : (
              <>
                <FiZap className="h-4 w-4" />
                Run Full Analysis
              </>
            )}
          </Button>
        </div>

        {isAnalyzing && (
          <div className="mt-6 flex flex-col items-center gap-2 text-center">
            <LoadingSpinner size="md" />
            <p className="text-sm text-slate-500">
              Running ATS scoring, skill extraction, and AI analysis...
            </p>
          </div>
        )}
      </Card>

      {parseResult && (
        <ParsedResumePreview
          parsedData={parseResult.parsed_data}
          metadata={parseResult.metadata}
        />
      )}

      {atsResult && (
        <Card glass>
          <CardHeader title="ATS Score Preview" subtitle="Weighted score before full AI analysis" />
          <ATSBreakdownPanel scores={atsResult.ats_scores} compact />
        </Card>
      )}

      {aiResult && (
        <Card glass>
          <CardHeader title="Gemini AI Preview" subtitle="AI feedback before full report save" />
          <AIFeedbackPanel feedback={aiResult.ai_feedback} compact />
        </Card>
      )}

      <div className="grid gap-4 sm:grid-cols-3">
        {[
          { title: 'PDF Parsing', desc: 'pdfplumber + PyPDF2 extraction' },
          { title: 'ATS Scoring', desc: '7-dimension weighted compatibility' },
          { title: 'Gemini AI', desc: 'Career coaching & resume insights' },
        ].map((item) => (
          <div key={item.title} className="rounded-xl border border-slate-200 p-4 text-center dark:border-slate-700">
            <p className="font-semibold text-slate-800 dark:text-white">{item.title}</p>
            <p className="mt-1 text-xs text-slate-500">{item.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
