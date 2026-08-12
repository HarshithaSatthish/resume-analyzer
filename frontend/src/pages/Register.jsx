import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FiBarChart2, FiUserPlus } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { getErrorMessage } from '../services/api';
import { validatePassword, validatePasswordMatch } from '../utils/validators';

export default function Register() {
  const [form, setForm] = useState({ full_name: '', email: '', password: '', confirmPassword: '' });
  const [errors, setErrors] = useState({});
  const { register, loading } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();

  const validate = () => {
    const newErrors = {};
    if (!form.full_name.trim()) newErrors.full_name = 'Full name is required.';
    if (form.full_name.trim().length < 2) newErrors.full_name = 'Name must be at least 2 characters.';
    if (!form.email.trim()) newErrors.email = 'Email is required.';
    if (!form.password) newErrors.password = 'Password is required.';
    else {
      const passwordError = validatePassword(form.password);
      if (passwordError) newErrors.password = passwordError;
    }
    const matchError = validatePasswordMatch(form.password, form.confirmPassword);
    if (matchError) newErrors.confirmPassword = matchError;
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validate()) return;

    try {
      await register({
        full_name: form.full_name.trim(),
        email: form.email.trim(),
        password: form.password,
      });
      toast.success('Account created successfully!');
      navigate('/dashboard');
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  return (
    <div className="flex min-h-screen">
      <div className="hidden w-1/2 bg-gradient-to-br from-accent-600 via-brand-600 to-brand-700 lg:flex lg:flex-col lg:justify-center lg:px-16">
        <div className="max-w-md text-white">
          <div className="mb-6 flex h-14 w-14 items-center justify-center rounded-2xl bg-white/20 backdrop-blur-sm">
            <FiBarChart2 className="h-7 w-7" />
          </div>
          <h1 className="text-4xl font-bold">Start Analyzing</h1>
          <p className="mt-4 text-lg text-brand-100">
            Join thousands of professionals optimizing their resumes with AI-powered insights.
          </p>
        </div>
      </div>

      <div className="flex flex-1 items-center justify-center px-4 py-12">
        <div className="w-full max-w-md animate-slide-up">
          <div className="mb-8 text-center lg:text-left">
            <h2 className="text-2xl font-bold text-slate-800 dark:text-white">Create account</h2>
            <p className="mt-1 text-sm text-slate-500">Get started with your free resume analysis</p>
          </div>

          <form onSubmit={handleSubmit} className="glass-card-solid space-y-5 p-6 sm:p-8">
            <Input
              label="Full Name"
              name="full_name"
              placeholder="John Doe"
              value={form.full_name}
              onChange={(e) => setForm({ ...form, full_name: e.target.value })}
              error={errors.full_name}
              autoComplete="name"
            />

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
              placeholder="Min. 8 chars, 1 letter & 1 number"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              error={errors.password}
              autoComplete="new-password"
            />

            <Input
              label="Confirm Password"
              name="confirmPassword"
              type="password"
              placeholder="Repeat password"
              value={form.confirmPassword}
              onChange={(e) => setForm({ ...form, confirmPassword: e.target.value })}
              error={errors.confirmPassword}
              autoComplete="new-password"
            />

            <Button type="submit" loading={loading} className="w-full">
              <FiUserPlus className="h-4 w-4" />
              Create Account
            </Button>
          </form>

          <p className="mt-6 text-center text-sm text-slate-500">
            Already have an account?{' '}
            <Link to="/login" className="font-semibold text-brand-600 hover:text-brand-700 dark:text-brand-400">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
