import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { FiFile, FiUploadCloud, FiX } from 'react-icons/fi';
import { ACCEPTED_FILE_TYPES, MAX_FILE_SIZE_BYTES, MAX_FILE_SIZE_MB } from '../../utils/constants';
import { formatFileSize } from '../../utils/formatters';
import { ProgressBar } from '../ui/ProgressBar';

export function ResumeDropzone({
  onFileSelect,
  selectedFile = null,
  disabled = false,
  uploadProgress = 0,
  isUploading = false,
}) {
  const [error, setError] = useState('');

  const onDrop = useCallback(
    (acceptedFiles, rejectedFiles) => {
      setError('');

      if (rejectedFiles.length > 0) {
        const rejection = rejectedFiles[0];
        if (rejection.errors[0]?.code === 'file-too-large') {
          setError(`File exceeds maximum size of ${MAX_FILE_SIZE_MB}MB.`);
        } else if (rejection.errors[0]?.code === 'file-invalid-type') {
          setError('Only PDF files are accepted.');
        } else {
          setError(rejection.errors[0]?.message || 'Invalid file.');
        }
        return;
      }

      const file = acceptedFiles[0];
      if (file) {
        onFileSelect?.(file);
      }
    },
    [onFileSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED_FILE_TYPES,
    maxSize: MAX_FILE_SIZE_BYTES,
    maxFiles: 1,
    disabled: disabled || isUploading,
  });

  const clearFile = (event) => {
    event.stopPropagation();
    setError('');
    onFileSelect?.(null);
  };

  return (
    <div className="space-y-3">
      <div
        {...getRootProps()}
        className={`relative cursor-pointer rounded-2xl border-2 border-dashed p-8 text-center transition-all duration-200
          ${isDragActive ? 'border-brand-500 bg-brand-50 dark:bg-brand-950/30' : 'border-slate-300 hover:border-brand-400 hover:bg-slate-50 dark:border-slate-600 dark:hover:border-brand-500 dark:hover:bg-slate-800/50'}
          ${disabled || isUploading ? 'cursor-not-allowed opacity-60' : ''}`}
      >
        <input {...getInputProps()} />

        {selectedFile ? (
          <div className="flex items-center justify-center gap-4">
            <div className="rounded-xl bg-brand-100 p-3 text-brand-600 dark:bg-brand-900/50 dark:text-brand-400">
              <FiFile className="h-8 w-8" />
            </div>
            <div className="text-left">
              <p className="font-semibold text-slate-800 dark:text-slate-100">{selectedFile.name}</p>
              <p className="text-sm text-slate-500">{formatFileSize(selectedFile.size)}</p>
            </div>
            {!isUploading && (
              <button
                type="button"
                onClick={clearFile}
                className="rounded-lg p-2 text-slate-400 transition-colors hover:bg-slate-100 hover:text-red-500 dark:hover:bg-slate-700"
                aria-label="Remove file"
              >
                <FiX className="h-5 w-5" />
              </button>
            )}
          </div>
        ) : (
          <div className="space-y-3">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-500 to-accent-500 text-white shadow-lg">
              <FiUploadCloud className="h-8 w-8" />
            </div>
            <div>
              <p className="text-lg font-semibold text-slate-700 dark:text-slate-200">
                {isDragActive ? 'Drop your resume here' : 'Drag & drop your resume'}
              </p>
              <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                Resume or CV only · PDF · Max {MAX_FILE_SIZE_MB}MB
              </p>
              <p className="mt-1 text-xs text-slate-400 dark:text-slate-500">
                Invoices, articles, manuals, and other PDFs are automatically rejected
              </p>
            </div>
          </div>
        )}
      </div>

      {error && <p className="text-sm text-red-500">{error}</p>}

      {isUploading && uploadProgress > 0 && (
        <ProgressBar value={uploadProgress} label="Uploading..." size="lg" />
      )}
    </div>
  );
}
