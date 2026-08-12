import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FiBarChart2, FiLock } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { getErrorMessage } from '../services/api';

export default function Login() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState({});
  const { login, loading } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();

  const validate = () => {
    const newErrors = {};
    if (!form.email.trim()) newErrors.email = 'Email is required.';
    if (!form.password) newErrors.password = 'Password is required.';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validate()) return;

    try {
      await login(form);
      toast.success('Welcome back!');
      navigate('/dashboard');
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  return (
    <div className="flex min-h-screen">
      <div className="hidden w-1/2 bg-gradient-to-br from-brand-600 via-brand-700 to-accent-600 lg:flex lg:flex-col lg:justify-center lg:px-16">
        <div className="max-w-md text-white">
          <div className="mb-6 flex h-14 w-14 items-center justify-center rounded-2xl bg-white/20 backdrop-blur-sm">
            <FiBarChart2 className="h-7 w-7" />
          </div>
          <h1 className="text-4xl font-bold">AI Resume Analyzer</h1>
          <p className="mt-4 text-lg text-brand-100">
            Get ATS scores, skill insights, and AI-powered career recommendations for your resume.
          </p>
          <ul className="mt-8 space-y-3 text-brand-100">
            <li className="flex items-center gap-2">✓ ATS compatibility scoring</li>
            <li className="flex items-center gap-2">✓ Skill extraction with spaCy NLP</li>
            <li className="flex items-center gap-2">✓ Gemini AI career insights</li>
          </ul>
        </div>
      </div>

      <div className="flex flex-1 items-center justify-center px-4 py-12">
        <div className="w-full max-w-md animate-slide-up">
          <div className="mb-8 text-center lg:text-left">
            <h2 className="text-2xl font-bold text-slate-800 dark:text-white">Sign in</h2>
            <p className="mt-1 text-sm text-slate-500">Enter your credentials to access your dashboard</p>
          </div>

          <form onSubmit={handleSubmit} className="glass-card-solid space-y-5 p-6 sm:p-8">
            <Input
              label="Email"
              name="email"
              type="email"
              placeholder="you@example.com"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              error={errors.email}
              autoComplete="email"
            />

            <Input
              label="Password"
              name="password"
              type="password"
              placeholder="••••••••"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              error={errors.password}
              autoComplete="current-password"
            />

            <Button type="submit" loading={loading} className="w-full">
              <FiLock className="h-4 w-4" />
              Sign In
            </Button>
          </form>

          <p className="mt-6 text-center text-sm text-slate-500">
            Don&apos;t have an account?{' '}
            <Link to="/register" className="font-semibold text-brand-600 hover:text-brand-700 dark:text-brand-400">
              Create one
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
