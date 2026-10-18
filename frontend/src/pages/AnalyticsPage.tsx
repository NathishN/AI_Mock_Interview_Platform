import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  TrendingUp,
  Award,
  BookOpen,
  Flame,
  AlertTriangle,
  Sparkles,
  BarChart2,
  Calendar,
  ArrowRight,
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  CartesianGrid,
} from 'recharts';
import {
  analyticsApi,
  AnalyticsOverview,
  SkillScore,
  ScoreHistoryPoint,
  WeakAreaItem,
} from '../api/analytics';

export const AnalyticsPage: React.FC = () => {
  const [overview, setOverview] = useState<AnalyticsOverview | null>(null);
  const [skills, setSkills] = useState<SkillScore[]>([]);
  const [history, setHistory] = useState<ScoreHistoryPoint[]>([]);
  const [weaknesses, setWeaknesses] = useState<WeakAreaItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      analyticsApi.getOverview().catch(() => null),
      analyticsApi.getSkills().catch(() => []),
      analyticsApi.getHistory().catch(() => []),
      analyticsApi.getWeaknesses().catch(() => []),
    ])
      .then(([ov, sk, hist, weak]) => {
        setOverview(ov);
        setSkills(sk);
        setHistory(hist);
        setWeaknesses(weak);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="py-24 text-center text-xs text-slate-500">
        <div className="w-7 h-7 border-3 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
        Calculating Placement Analytics & Trend Models...
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto py-6 space-y-8">
      {/* Header */}
      <div className="space-y-1.5">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400">
          <TrendingUp className="w-3.5 h-3.5" />
          Placement Readiness Intelligence
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
          Progress & Performance Analytics
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
          Track objective rubric scores over time, identify persistent blind spots, and monitor campus placement readiness.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1">
          <span className="text-xs text-slate-400 font-medium">Readiness Score</span>
          <div className="text-2xl font-bold text-brand-600 dark:text-brand-400">
            {overview?.readiness_score ?? 0}%
          </div>
          <span className="text-[11px] text-slate-500">
            Band: {overview?.performance_band || 'In Progress'}
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1">
          <span className="text-xs text-slate-400 font-medium">Average Mark</span>
          <div className="text-2xl font-bold text-slate-900 dark:text-white">
            {overview?.average_score ? `${overview.average_score}/100` : '--/100'}
          </div>
          <span className="text-[11px] text-slate-500">Across all turns</span>
        </div>

        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1">
          <span className="text-xs text-slate-400 font-medium">Questions Answered</span>
          <div className="text-2xl font-bold text-slate-900 dark:text-white">
            {overview?.total_questions_answered ?? 0}
          </div>
          <span className="text-[11px] text-slate-500">
            {overview?.completed_sessions ?? 0} completed rounds
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1">
          <span className="text-xs text-slate-400 font-medium">Active Streak</span>
          <div className="text-2xl font-bold text-rose-500">
            {overview?.current_streak_days ?? 0} Days
          </div>
          <span className="text-[11px] text-slate-500">Daily practice active</span>
        </div>
      </div>

      {/* Historical Score Progression Line Chart */}
      <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-brand-500" />
            Interview Score Progression Over Time
          </h2>
          <span className="text-xs text-slate-400">Target Benchmark: 80%</span>
        </div>

        {history.length === 0 ? (
          <div className="py-12 text-center text-xs text-slate-400">
            Complete at least one mock interview round to view your historical trend curve.
          </div>
        ) : (
          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={history} margin={{ top: 10, right: 20, left: -20, bottom: 10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="date" tick={{ fontSize: 11 }} stroke="#94a3b8" />
                <YAxis domain={[0, 100]} ticks={[0, 25, 50, 75, 100]} tick={{ fontSize: 11 }} stroke="#94a3b8" />
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const pt = payload[0].payload;
                      return (
                        <div className="p-2.5 rounded-xl bg-slate-900 text-white text-xs shadow-lg space-y-0.5">
                          <div className="font-bold">{pt.role}</div>
                          <div>Score: {pt.score}/100</div>
                          <div className="text-[10px] text-slate-400">{pt.date}</div>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#0c87eb"
                  strokeWidth={3}
                  dot={{ r: 4, fill: '#0c87eb' }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Skill Category Breakdown */}
      <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <BarChart2 className="w-4 h-4 text-indigo-500" />
            Performance by Competency Category
          </h2>
          <span className="text-xs text-slate-400">Average Dimension Marks</span>
        </div>

        {skills.length === 0 ? (
          <div className="py-12 text-center text-xs text-slate-400">
            No competency scores logged yet.
          </div>
        ) : (
          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={skills} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <XAxis dataKey="category" tick={{ fontSize: 10 }} stroke="#94a3b8" />
                <YAxis domain={[0, 100]} stroke="#94a3b8" tick={{ fontSize: 11 }} />
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const item = payload[0].payload;
                      return (
                        <div className="p-2.5 rounded-xl bg-slate-900 text-white text-xs shadow-lg space-y-0.5">
                          <div className="font-bold">{item.category}</div>
                          <div>Average: {item.score}% ({item.total_evaluated} questions)</div>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Bar dataKey="score" fill="#6366f1" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Persistent Weak Areas & Remediation */}
      <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-500" />
            Detected Weak Areas & Recommended Fixes
          </h2>
          <span className="text-xs text-slate-400">{weaknesses.length} flagged areas</span>
        </div>

        {weaknesses.length === 0 ? (
          <div className="p-6 rounded-2xl bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-100 dark:border-emerald-900 text-xs text-emerald-800 dark:text-emerald-300">
            Great job! No severe weaknesses or recurring failures detected so far. Keep practicing to maintain your streak.
          </div>
        ) : (
          <div className="space-y-3">
            {weaknesses.map((item, idx) => (
              <div
                key={idx}
                className="p-4 rounded-2xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/40 text-xs space-y-2"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-900 dark:text-white">
                    {item.topic} ({item.category})
                  </span>
                  <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-amber-50 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400">
                    Average: {item.average_score}% • {item.frequency} Occurrences
                  </span>
                </div>
                <p className="text-slate-600 dark:text-slate-300">
                  {item.recommendation}
                </p>
                <div className="pt-1">
                  <Link
                    to="/library"
                    className="inline-flex items-center gap-1 font-semibold text-brand-600 dark:text-brand-400 hover:underline text-[11px]"
                  >
                    Open Library & Review Model Answers
                    <ArrowRight className="w-3 h-3" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
