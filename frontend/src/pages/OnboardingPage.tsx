import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { Sparkles, ArrowRight, CheckCircle2 } from 'lucide-react';
import { profileApi } from '../api/profile';

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

const WEAKNESS_AREAS = [
  'HR & Self-Introduction',
  'STAR Behavioral Answers',
  'Data Structures & Algorithms',
  'Explaining Resume Projects',
  'System Design & OOP',
  'SQL & Database Queries',
  'Handling Rejection / Anxiety',
];

export const OnboardingPage: React.FC = () => {
  const navigate = useNavigate();
  const [selectedCompanies, setSelectedCompanies] = useState<string[]>(['TCS', 'Amazon']);
  const [selectedWeaknesses, setSelectedWeaknesses] = useState<string[]>([
    'HR & Self-Introduction',
    'Explaining Resume Projects',
  ]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { register, handleSubmit } = useForm({
    defaultValues: {
      degree: 'B.Tech',
      branch: 'Computer Science and Engineering',
      graduation_year: 2025,
      target_role: 'Software Development Engineer',
      interview_experience: 'Beginner (0-2 interviews)',
      preferred_language: 'Python',
      daily_prep_minutes: 30,
      interview_goals: 'Clear campus placements and secure an SDE role at a top technology company.',
    },
  });

  const toggleCompany = (comp: string) => {
    setSelectedCompanies((prev) =>
      prev.includes(comp) ? prev.filter((c) => c !== comp) : [...prev, comp]
    );
  };

  const toggleWeakness = (weak: string) => {
    setSelectedWeaknesses((prev) =>
      prev.includes(weak) ? prev.filter((w) => w !== weak) : [...prev, weak]
    );
  };

  const onSubmit = async (values: any) => {
    try {
      setIsSubmitting(true);
      await profileApi.updateProfile({
        ...values,
        graduation_year: Number(values.graduation_year),
        daily_prep_minutes: Number(values.daily_prep_minutes),
        preferred_companies: selectedCompanies,
        weakness_areas: selectedWeaknesses,
      });
      navigate('/dashboard');
    } catch (err) {
      console.error(err);
      navigate('/dashboard'); // fallback navigate even if mock or network glitch
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8 sm:p-10 shadow-xl space-y-8">
        <div className="space-y-2 border-b border-slate-200 dark:border-slate-800 pb-6">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400">
            <Sparkles className="w-3.5 h-3.5" />
            Personalized Placement Setup
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white">
            Tailor Your Interview Preparation
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
            Provide your academic profile and interview goals so InterviewAce can personalize your mock interview difficulty and questions.
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Degree & Academic Info */}
          <div className="grid sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Degree
              </label>
              <input
                type="text"
                {...register('degree')}
                placeholder="e.g. B.Tech / B.E. / BCA / MCA"
                className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Branch / Specialization
              </label>
              <input
                type="text"
                {...register('branch')}
                placeholder="e.g. Computer Science, IT, ECE"
                className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Graduation Year
              </label>
              <input
                type="number"
                {...register('graduation_year')}
                placeholder="2025"
                className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
              />
            </div>
          </div>

          {/* Target Role & Coding Language */}
          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Target Job Role
              </label>
              <select
                {...register('target_role')}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
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
                Primary Programming Language
              </label>
              <select
                {...register('preferred_language')}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
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
              Preferred Companies for Campus Placement
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
                    {isSelected && <CheckCircle2 className="w-3.5 h-3.5" />}
                    {comp}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Weakness Areas */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
              Areas Where You Need Targeted Coaching
            </label>
            <div className="flex flex-wrap gap-2">
              {WEAKNESS_AREAS.map((weak) => {
                const isSelected = selectedWeaknesses.includes(weak);
                return (
                  <button
                    key={weak}
                    type="button"
                    onClick={() => toggleWeakness(weak)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors flex items-center gap-1.5 ${
                      isSelected
                        ? 'bg-amber-50 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400 border-amber-300 dark:border-amber-800'
                        : 'border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800'
                    }`}
                  >
                    {isSelected && <CheckCircle2 className="w-3.5 h-3.5" />}
                    {weak}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Daily prep time & Interview Goals */}
          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Daily Prep Time Allocation
              </label>
              <select
                {...register('daily_prep_minutes')}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
              >
                <option value={15}>15 minutes / day</option>
                <option value={30}>30 minutes / day</option>
                <option value={45}>45 minutes / day</option>
                <option value={60}>60+ minutes / day</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Your Primary Goal
              </label>
              <input
                type="text"
                {...register('interview_goals')}
                placeholder="e.g. Clear TCS Digital or product company interview"
                className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
              />
            </div>
          </div>

          <div className="pt-4 border-t border-slate-200 dark:border-slate-800">
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full py-3.5 px-6 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-semibold text-xs shadow-md shadow-brand-500/20 transition-all flex items-center justify-center gap-2"
            >
              {isSubmitting ? 'Saving Profile...' : 'Complete Setup & Go to Dashboard'}
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
