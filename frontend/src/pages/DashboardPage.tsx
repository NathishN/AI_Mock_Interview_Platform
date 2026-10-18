import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Mic,
  MessageSquare,
  BookOpen,
  Building2,
  TrendingUp,
  Award,
  Zap,
  Clock,
  ArrowRight,
  Sparkles,
  ChevronRight,
  Flame,
  CheckCircle2,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { analyticsApi, AnalyticsOverview } from '../api/analytics';
import { interviewsApi, InterviewSessionSummary } from '../api/interviews';
import { profileApi, UserProfile } from '../api/profile';

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [overview, setOverview] = useState<AnalyticsOverview | null>(null);
  const [sessions, setSessions] = useState<InterviewSessionSummary[]>([]);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [ov, sess, prof] = await Promise.all([
          analyticsApi.getOverview().catch(() => null),
          interviewsApi.listSessions(5).catch(() => []),
          profileApi.getProfile().catch(() => null),
        ]);
        setOverview(ov);
        setSessions(sess);
        setProfile(prof);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="space-y-8 py-4">
      {/* Welcome Banner */}
      <div className="p-6 sm:p-8 rounded-3xl bg-gradient-to-r from-brand-900 via-brand-800 to-indigo-900 text-white shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 translate-x-8 -translate-y-8 w-64 h-64 bg-brand-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-white/10 backdrop-blur-md text-brand-200 border border-white/10">
              <Sparkles className="w-3.5 h-3.5" />
              Target Role: {profile?.target_role || 'Software Development Engineer'}
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
              Welcome back, {user?.full_name?.split(' ')[0] || 'Candidate'}!
            </h1>
            <p className="text-xs sm:text-sm text-slate-300 max-w-xl">
              Consistent practice is the key to clearing technical screening and HR rounds. Your current placement readiness is{' '}
              <span className="font-bold text-white">{overview?.readiness_score || 0}%</span>.
            </p>
          </div>

          <div className="flex sm:flex-col items-center sm:items-end justify-between border-t sm:border-t-0 border-white/10 pt-4 sm:pt-0">
            <Link
              to="/interview/new"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white text-brand-900 hover:bg-slate-100 font-bold text-xs shadow-md transition-all hover:scale-105"
            >
              <Mic className="w-4 h-4 text-brand-600" />
              Start Mock Interview
            </Link>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* KPI 1 */}
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400">
            <span className="text-xs font-medium">Readiness Score</span>
            <TrendingUp className="w-4 h-4 text-brand-500" />
          </div>
          <div className="text-2xl font-bold text-slate-900 dark:text-white">
            {overview?.readiness_score ?? 0}%
          </div>
          <div className="text-[11px] text-brand-600 dark:text-brand-400 font-medium">
            Band: {overview?.performance_band || 'In Progress'}
          </div>
        </div>

        {/* KPI 2 */}
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400">
            <span className="text-xs font-medium">Average Mark</span>
            <Award className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-bold text-slate-900 dark:text-white">
            {overview?.average_score ? `${overview.average_score}/100` : '--/100'}
          </div>
          <div className="text-[11px] text-slate-500 dark:text-slate-400">
            Across evaluated turns
          </div>
        </div>

        {/* KPI 3 */}
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400">
            <span className="text-xs font-medium">Questions Practiced</span>
            <BookOpen className="w-4 h-4 text-indigo-500" />
          </div>
          <div className="text-2xl font-bold text-slate-900 dark:text-white">
            {overview?.total_questions_answered ?? 0}
          </div>
          <div className="text-[11px] text-slate-500 dark:text-slate-400">
            Out of 500 in Library
          </div>
        </div>

        {/* KPI 4 */}
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1">
          <div className="flex items-center justify-between text-slate-500 dark:text-slate-400">
            <span className="text-xs font-medium">Practice Streak</span>
            <Flame className="w-4 h-4 text-rose-500 fill-rose-500" />
          </div>
          <div className="text-2xl font-bold text-slate-900 dark:text-white">
            {overview?.current_streak_days ?? 0} Days
          </div>
          <div className="text-[11px] text-rose-600 dark:text-rose-400 font-medium">
            Daily target: {profile?.daily_prep_minutes || 30} mins
          </div>
        </div>
      </div>

      {/* Main Actions Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Link
          to="/interview/new"
          className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-brand-500/60 transition-all hover:shadow-md group space-y-3"
        >
          <div className="w-10 h-10 rounded-xl bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400 flex items-center justify-center font-bold group-hover:scale-105 transition-transform">
            <Mic className="w-5 h-5" />
          </div>
          <div className="space-y-1">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center justify-between">
              Mock Interview Room
              <ChevronRight className="w-4 h-4 text-slate-400 group-hover:translate-x-1 transition-transform" />
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Adaptive difficulty, real-time rubric marks & speech-to-text input.
            </p>
          </div>
        </Link>

        <Link
          to="/hr-studio"
          className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-indigo-500/60 transition-all hover:shadow-md group space-y-3"
        >
          <div className="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center font-bold group-hover:scale-105 transition-transform">
            <MessageSquare className="w-5 h-5" />
          </div>
          <div className="space-y-1">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center justify-between">
              HR Answer Studio
              <ChevronRight className="w-4 h-4 text-slate-400 group-hover:translate-x-1 transition-transform" />
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Build and critique self-intro & weaknesses without clichés.
            </p>
          </div>
        </Link>

        <Link
          to="/company-prep"
          className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-emerald-500/60 transition-all hover:shadow-md group space-y-3"
        >
          <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center font-bold group-hover:scale-105 transition-transform">
            <Building2 className="w-5 h-5" />
          </div>
          <div className="space-y-1">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center justify-between">
              Company-Specific Prep
              <ChevronRight className="w-4 h-4 text-slate-400 group-hover:translate-x-1 transition-transform" />
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Hiring rounds, focus areas, and guides for TCS, Infosys, Amazon, etc.
            </p>
          </div>
        </Link>

        <Link
          to="/library"
          className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-amber-500/60 transition-all hover:shadow-md group space-y-3"
        >
          <div className="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400 flex items-center justify-center font-bold group-hover:scale-105 transition-transform">
            <BookOpen className="w-5 h-5" />
          </div>
          <div className="space-y-1">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center justify-between">
              500-Question Library
              <ChevronRight className="w-4 h-4 text-slate-400 group-hover:translate-x-1 transition-transform" />
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Curated reference answers, common mistakes & key evaluation points.
            </p>
          </div>
        </Link>
      </div>

      {/* Recent Sessions & Weak Areas Section */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Recent Sessions (2 columns) */}
        <div className="lg:col-span-2 p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Clock className="w-4 h-4 text-brand-500" />
              Recent Mock Interviews
            </h2>
            <Link to="/analytics" className="text-xs font-semibold text-brand-600 hover:underline">
              View History
            </Link>
          </div>

          {sessions.length === 0 ? (
            <div className="text-center py-8 text-xs text-slate-500 dark:text-slate-400 space-y-3">
              <p>No mock interview sessions completed yet.</p>
              <Link
                to="/interview/new"
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-brand-600 text-white font-semibold text-xs"
              >
                Launch Your First Session
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          ) : (
            <div className="divide-y divide-slate-100 dark:divide-slate-800">
              {sessions.map((sess) => (
                <div key={sess.id} className="py-3 flex items-center justify-between gap-4">
                  <div className="space-y-0.5">
                    <div className="text-xs font-bold text-slate-800 dark:text-slate-200">
                      {sess.config?.target_role || 'General Interview'} • {sess.config?.mode || 'Mixed'}
                    </div>
                    <div className="text-[11px] text-slate-500 dark:text-slate-400">
                      Preset: {sess.config?.preset || 'Custom'} • {new Date(sess.created_at).toLocaleDateString()}
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <span
                      className={`text-xs font-bold px-2.5 py-1 rounded-full ${
                        sess.status === 'completed'
                          ? 'bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400'
                          : 'bg-amber-50 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400'
                      }`}
                    >
                      {sess.status === 'completed'
                        ? sess.final_score != null
                          ? `${sess.final_score}/100`
                          : 'Completed'
                        : 'In Progress'}
                    </span>
                    <Link
                      to={
                        sess.status === 'completed'
                          ? `/interview/${sess.id}/results`
                          : `/interview/${sess.id}`
                      }
                      className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-200"
                    >
                      <ChevronRight className="w-4 h-4" />
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Target Focus & Weak Areas Card */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
          <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Zap className="w-4 h-4 text-amber-500" />
            Target Focus Areas
          </h2>

          <div className="space-y-3">
            {(profile?.weakness_areas || [
              'HR & Self-Introduction',
              'Explaining Resume Projects',
            ]).map((area, idx) => (
              <div
                key={idx}
                className="p-3 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/40 text-xs flex items-center justify-between"
              >
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-amber-500"></div>
                  <span className="font-medium text-slate-800 dark:text-slate-200">{area}</span>
                </div>
                <Link
                  to="/library"
                  className="text-[11px] font-semibold text-brand-600 hover:underline"
                >
                  Practice
                </Link>
              </div>
            ))}
          </div>

          <div className="pt-2">
            <Link
              to="/roadmap"
              className="w-full py-2.5 px-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 font-semibold text-xs flex items-center justify-center gap-1.5 transition-colors"
            >
              View 4-Week Prep Roadmap
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};
