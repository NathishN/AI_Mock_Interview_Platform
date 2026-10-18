import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import {
  Settings,
  User,
  Sparkles,
  CheckCircle,
  Moon,
  Sun,
  LogOut,
  Save,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { profileApi, UserProfile } from '../api/profile';

const TARGET_ROLES = [
  'Software Development Engineer',
  'Python Developer',
  'Java Developer',
  'Data Analyst',
  'Data Scientist',
  'Machine Learning Engineer',
  'AI Engineer',
  'Generative AI Engineer',
  'Full-Stack Developer',
  'Backend Developer',
  'Business Analyst',
  'Other',
];

const POPULAR_COMPANIES = [
  'TCS',
  'Infosys',
  'Amazon',
  'Google',
  'Microsoft',
  'Accenture',
  'Wipro',
  'Cognizant',
  'Capgemini',
];

export const SettingsPage: React.FC = () => {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  const [savedSuccess, setSavedSuccess] = useState(false);
  const [selectedCompanies, setSelectedCompanies] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  const { register, handleSubmit, reset } = useForm();

  useEffect(() => {
    profileApi
      .getProfile()
      .then((data) => {
        reset({
          degree: data.degree || '',
          branch: data.branch || '',
          graduation_year: data.graduation_year || 2025,
          target_role: data.target_role || 'Software Development Engineer',
          preferred_language: data.preferred_language || 'Python',
          daily_prep_minutes: data.daily_prep_minutes || 30,
          interview_goals: data.interview_goals || '',
        });
        setSelectedCompanies(data.preferred_companies || ['TCS', 'Amazon']);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, [reset]);

  const toggleCompany = (comp: string) => {
    setSelectedCompanies((prev) =>
      prev.includes(comp) ? prev.filter((c) => c !== comp) : [...prev, comp]
    );
  };

  const onSubmit = async (values: any) => {
    try {
      setSavedSuccess(false);
      await profileApi.updateProfile({
        ...values,
        graduation_year: Number(values.graduation_year),
        daily_prep_minutes: Number(values.daily_prep_minutes),
        preferred_companies: selectedCompanies,
      });
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="py-24 text-center text-xs text-slate-500">
        <div className="w-7 h-7 border-3 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
        Loading User Settings...
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto py-6 space-y-8">
      {/* Header */}
      <div className="space-y-1.5">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400">
          <Settings className="w-3.5 h-3.5" />
          User Preferences
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
          Profile & Application Settings
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
          Manage your placement profile details, target recruiter preferences, and UI theme.
        </p>
      </div>

      {savedSuccess && (
        <div className="p-3.5 rounded-2xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300 text-xs flex items-center gap-2">
          <CheckCircle className="w-4 h-4 shrink-0" />
          <span>Profile changes saved successfully!</span>
        </div>
      )}

      {/* Account Info Box */}
      <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
        <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
          Account Credentials
        </h2>
        <div className="grid sm:grid-cols-2 gap-4 text-xs">
          <div>
            <span className="text-slate-400">Full Name</span>
            <div className="font-semibold text-slate-900 dark:text-white mt-0.5">
              {user?.full_name}
            </div>
          </div>
          <div>
            <span className="text-slate-400">Email Address</span>
            <div className="font-semibold text-slate-900 dark:text-white mt-0.5">
              {user?.email}
            </div>
          </div>
        </div>
      </div>

      {/* Profile Form */}
      <form onSubmit={handleSubmit(onSubmit)} className="p-6 sm:p-8 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-6">
        <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
          Academic & Interview Customization
        </h2>

        <div className="grid sm:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Degree
            </label>
            <input
              type="text"
              {...register('degree')}
              className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Branch / Specialization
            </label>
            <input
              type="text"
              {...register('branch')}
              className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Graduation Year
            </label>
            <input
              type="number"
              {...register('graduation_year')}
              className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
            />
          </div>
        </div>

        <div className="grid sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Target Job Role
            </label>
            <select
              {...register('target_role')}
              className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
            >
              {TARGET_ROLES.map((role) => (
                <option key={role} value={role}>
                  {role}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Primary Language
            </label>
            <select
              {...register('preferred_language')}
              className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
            >
              <option value="Python">Python</option>
              <option value="Java">Java</option>
              <option value="C++">C++</option>
              <option value="JavaScript / TypeScript">JavaScript / TypeScript</option>
            </select>
          </div>
        </div>

        {/* Preferred Companies */}
        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
            Target Recruiters
          </label>
          <div className="flex flex-wrap gap-2">
            {POPULAR_COMPANIES.map((comp) => {
              const isSelected = selectedCompanies.includes(comp);
              return (
                <button
                  key={comp}
                  type="button"
                  onClick={() => toggleCompany(comp)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors flex items-center gap-1.5 ${
                    isSelected
                      ? 'bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400 border-brand-300 dark:border-brand-800'
                      : 'border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800'
                  }`}
                >
                  {comp}
                </button>
              );
            })}
          </div>
        </div>

        {/* Daily Prep & Goals */}
        <div className="grid sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Daily Prep Time (Minutes)
            </label>
            <select
              {...register('daily_prep_minutes')}
              className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
            >
              <option value={15}>15 minutes</option>
              <option value={30}>30 minutes</option>
              <option value={45}>45 minutes</option>
              <option value={60}>60+ minutes</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Primary Goal Statement
            </label>
            <input
              type="text"
              {...register('interview_goals')}
              placeholder="e.g. Crack product company SDE interview"
              className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
            />
          </div>
        </div>

        <div className="pt-2">
          <button
            type="submit"
            className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs shadow-md transition-all"
          >
            <Save className="w-3.5 h-3.5" />
            Save Profile Preferences
          </button>
        </div>
      </form>

      {/* Theme & Display Box */}
      <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm flex items-center justify-between gap-4">
        <div>
          <div className="text-xs font-bold text-slate-900 dark:text-white">
            Interface Appearance
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Currently using {theme === 'dark' ? 'Dark Mode' : 'Light Mode'}.
          </p>
        </div>
        <button
          onClick={toggleTheme}
          className="flex items-center gap-2 px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 text-xs font-semibold hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        >
          {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-500" /> : <Moon className="w-4 h-4" />}
          Toggle {theme === 'dark' ? 'Light' : 'Dark'} Mode
        </button>
      </div>

      {/* Logout Box */}
      <div className="p-6 rounded-3xl bg-rose-50/40 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/40 flex items-center justify-between gap-4">
        <div>
          <div className="text-xs font-bold text-rose-800 dark:text-rose-400">
            Sign Out
          </div>
          <p className="text-xs text-rose-600/80 dark:text-rose-400/80">
            End your current session on this device.
          </p>
        </div>
        <button
          onClick={logout}
          className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs transition-colors"
        >
          <LogOut className="w-3.5 h-3.5" />
          Sign Out
        </button>
      </div>
    </div>
  );
};
