import { Link } from 'react-router-dom';
import { FiArrowLeft, FiAlertTriangle } from 'react-icons/fi';
import { Button } from '../components/ui/Button';

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-4 text-center">
      <div className="animate-slide-up">
        <p className="text-8xl font-bold gradient-text">404</p>
        <h1 className="mt-4 text-2xl font-bold text-slate-800 dark:text-white">Page Not Found</h1>
        <p className="mt-2 max-w-md text-slate-500">
          The page you&apos;re looking for doesn&apos;t exist or has been moved.
        </p>
        <Link to="/dashboard" className="mt-8 inline-block">
          <Button>
            <FiArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </Button>
        </Link>
      </div>
    </div>
  );
}

export function ErrorPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-4 text-center">
      <div className="animate-slide-up">
        <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-red-100 dark:bg-red-950/30">
          <FiAlertTriangle className="h-10 w-10 text-red-500" />
        </div>
        <h1 className="text-2xl font-bold text-slate-800 dark:text-white">Something Went Wrong</h1>
        <p className="mt-2 max-w-md text-slate-500">
          An unexpected error occurred. Please try again or contact support if the problem persists.
        </p>
        <div className="mt-8 flex justify-center gap-3">
          <Button onClick={() => window.location.reload()}>Try Again</Button>
          <Link to="/dashboard">
            <Button variant="secondary">
              <FiArrowLeft className="h-4 w-4" />
              Dashboard
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
