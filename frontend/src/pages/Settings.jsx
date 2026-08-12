import { useState } from 'react';
import { FiKey, FiLock, FiMoon, FiSave, FiSun, FiUser } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { useToast } from '../context/ToastContext';
import { Button } from '../components/ui/Button';
import { Card, CardHeader } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { getErrorMessage } from '../services/api';
import { formatDate } from '../utils/formatters';
import { validatePassword, validatePasswordMatch } from '../utils/validators';

export default function Settings() {
  const { user, updateProfile, updateSettings, changePassword } = useAuth();
  const { setTheme, isDark } = useTheme();
  const toast = useToast();

  const [fullName, setFullName] = useState(user?.full_name || '');
  const [apiKey, setApiKey] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [savingProfile, setSavingProfile] = useState(false);
  const [savingSettings, setSavingSettings] = useState(false);
  const [savingPassword, setSavingPassword] = useState(false);

  const [passwordForm, setPasswordForm] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
  });
  const [passwordErrors, setPasswordErrors] = useState({});

  const handleSaveProfile = async () => {
    if (!fullName.trim() || fullName.trim().length < 2) {
      toast.error('Full name must be at least 2 characters.');
      return;
    }

    setSavingProfile(true);
    try {
      await updateProfile({ full_name: fullName.trim() });
      toast.success('Profile updated successfully.');
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setSavingProfile(false);
    }
  };

  const handleSaveApiKey = async () => {
    setSavingSettings(true);
    try {
      await updateSettings({ gemini_api_key: apiKey.trim() || null });
      setApiKey('');
      toast.success('Gemini API key saved to your account.');
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setSavingSettings(false);
    }
  };

  const handleClearApiKey = async () => {
    setSavingSettings(true);
    try {
      await updateSettings({ gemini_api_key: null });
      setApiKey('');
      toast.info('Gemini API key removed from your account.');
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setSavingSettings(false);
    }
  };

  const handleChangePassword = async (event) => {
    event.preventDefault();
    const errors = {};

    const newPasswordError = validatePassword(passwordForm.new_password);
    if (newPasswordError) errors.new_password = newPasswordError;

    const matchError = validatePasswordMatch(passwordForm.new_password, passwordForm.confirm_password);
    if (matchError) errors.confirm_password = matchError;

    if (!passwordForm.current_password) {
      errors.current_password = 'Current password is required.';
    }

    setPasswordErrors(errors);
    if (Object.keys(errors).length > 0) return;

    setSavingPassword(true);
    try {
      await changePassword({
        current_password: passwordForm.current_password,
        new_password: passwordForm.new_password,
      });
      toast.success('Password changed successfully.');
      setPasswordForm({ current_password: '', new_password: '', confirm_password: '' });
      setPasswordErrors({});
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setSavingPassword(false);
    }
  };

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-800 dark:text-white">
          <span className="gradient-text">Settings</span>
        </h2>
        <p className="mt-1 text-sm text-slate-500">Manage your profile, security, and preferences</p>
      </div>

      <Card glass>
        <CardHeader title="Profile" subtitle="Update your account information" />
        <div className="space-y-4">
          <div className="flex items-center gap-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-500 to-accent-500 text-2xl font-bold text-white">
              {user?.full_name?.charAt(0)?.toUpperCase() || 'U'}
            </div>
            <div>
              <p className="text-sm text-slate-500">{user?.email}</p>
              {user?.created_at && (
                <p className="text-xs text-slate-400">Member since {formatDate(user.created_at)}</p>
              )}
            </div>
          </div>

          <Input
            label="Full Name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            placeholder="Your full name"
          />

          <div className="rounded-xl bg-slate-50 p-3 dark:bg-slate-800/50">
            <div className="flex items-center gap-2 text-xs font-medium text-slate-500">
              <FiUser className="h-3.5 w-3.5" /> Email
            </div>
            <p className="mt-1 text-sm font-medium text-slate-800 dark:text-white">{user?.email}</p>
          </div>

          <Button onClick={handleSaveProfile} loading={savingProfile}>
            <FiSave className="h-4 w-4" /> Save Profile
          </Button>
        </div>
      </Card>

      <Card glass>
        <CardHeader title="Change Password" subtitle="Update your account password" />
        <form onSubmit={handleChangePassword} className="space-y-4">
          <Input
            label="Current Password"
            type="password"
            value={passwordForm.current_password}
            onChange={(e) => setPasswordForm({ ...passwordForm, current_password: e.target.value })}
            error={passwordErrors.current_password}
            autoComplete="current-password"
          />
          <Input
            label="New Password"
            type="password"
            value={passwordForm.new_password}
            onChange={(e) => setPasswordForm({ ...passwordForm, new_password: e.target.value })}
            error={passwordErrors.new_password}
            autoComplete="new-password"
          />
          <Input
            label="Confirm New Password"
            type="password"
            value={passwordForm.confirm_password}
            onChange={(e) => setPasswordForm({ ...passwordForm, confirm_password: e.target.value })}
            error={passwordErrors.confirm_password}
            autoComplete="new-password"
          />
          <Button type="submit" loading={savingPassword}>
            <FiLock className="h-4 w-4" /> Update Password
          </Button>
        </form>
      </Card>

      <Card glass>
        <CardHeader title="Appearance" subtitle="Customize the interface" />
        <div className="flex items-center justify-between rounded-xl border border-slate-200 p-4 dark:border-slate-700">
          <div className="flex items-center gap-3">
            {isDark ? <FiMoon className="h-5 w-5 text-brand-500" /> : <FiSun className="h-5 w-5 text-amber-500" />}
            <div>
              <p className="font-medium text-slate-800 dark:text-white">Dark Mode</p>
              <p className="text-xs text-slate-500">{isDark ? 'Dark theme active' : 'Light theme active'}</p>
            </div>
          </div>
          <button
            type="button"
            onClick={() => setTheme(isDark ? 'light' : 'dark')}
            className={`relative h-7 w-12 rounded-full transition-colors ${isDark ? 'bg-brand-600' : 'bg-slate-300'}`}
            aria-label="Toggle dark mode"
          >
            <span
              className={`absolute top-0.5 h-6 w-6 rounded-full bg-white shadow transition-transform ${isDark ? 'translate-x-5' : 'translate-x-0.5'}`}
            />
          </button>
        </div>
      </Card>

      <Card glass>
        <CardHeader
          title="Gemini API Key"
          subtitle={
            user?.has_gemini_api_key
              ? 'A custom API key is configured on your account'
              : 'Optional — use your own Gemini key for AI feedback'
          }
        />
        <div className="space-y-4">
          <div className="relative">
            <FiKey className="absolute left-3 top-[38px] h-4 w-4 text-slate-400" />
            <Input
              label="API Key"
              type={showKey ? 'text' : 'password'}
              placeholder="Enter your Google Gemini API key"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="pl-10"
            />
          </div>
          <label className="flex items-center gap-2 text-sm text-slate-500">
            <input
              type="checkbox"
              checked={showKey}
              onChange={(e) => setShowKey(e.target.checked)}
              className="rounded border-slate-300"
            />
            Show key
          </label>
          <div className="flex gap-2">
            <Button onClick={handleSaveApiKey} loading={savingSettings}>
              <FiSave className="h-4 w-4" /> Save Key
            </Button>
            <Button variant="secondary" onClick={handleClearApiKey} loading={savingSettings}>
              Clear
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}
