import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Award,
  Sparkles,
  TrendingUp,
  CheckCircle,
  AlertCircle,
  BookOpen,
  ArrowRight,
  RotateCcw,
  BarChart2,
  HelpCircle,
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
} from 'recharts';
import { interviewsApi, InterviewReport } from '../api/interviews';

export const InterviewResultsPage: React.FC = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const [report, setReport] = useState<InterviewReport | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (sessionId) {
      interviewsApi
        .getReport(sessionId)
        .then((res) => setReport(res))
        .catch((err) => console.error(err))
        .finally(() => setLoading(false));
    }
  }, [sessionId]);

  if (loading) {
    return (
      <div className="py-24 text-center text-xs text-slate-500">
        <div className="w-7 h-7 border-3 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
        Synthesizing Comprehensive Performance Report...
      </div>
    );
  }

  if (!report) {
    return (
      <div className="py-20 text-center space-y-3">
        <p className="text-xs text-slate-500">Interview report not found.</p>
        <Link to="/dashboard" className="text-xs font-bold text-brand-600 hover:underline">
          Return to Dashboard
        </Link>
      </div>
    );
  }

  // Chart data formatting
  const chartData = report.dimension_breakdown.map((d) => ({
    name: d.dimension,
    score: d.average_mark, // 0-10
    percentage: d.percentage, // 0-100%
  }));

  const getScoreColor = (score: number) => {
    if (score >= 80) return '#10b981'; // emerald
    if (score >= 70) return '#0ea5e9'; // sky
    if (score >= 60) return '#f59e0b'; // amber
    return '#f43f5e'; // rose
  };

  return (
    <div className="max-w-4xl mx-auto py-6 space-y-8">
      {/* Top Hero Banner */}
      <div className="p-8 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xl flex flex-col sm:flex-row items-center justify-between gap-6">
        <div className="space-y-2 text-center sm:text-left">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400">
            <Sparkles className="w-3.5 h-3.5" />
            Interview Performance Report
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
            Placement Assessment Summary
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 max-w-md">
            Evaluation synthesized from deterministic rubric marks across {report.total_questions} interview questions.
          </p>
        </div>

        {/* Big Score Badge */}
        <div className="flex flex-col items-center justify-center p-6 rounded-2xl bg-gradient-to-tr from-brand-50 to-indigo-50 dark:from-slate-800 dark:to-slate-800/60 border border-brand-200 dark:border-slate-700 min-w-[180px]">
          <span className="text-4xl sm:text-5xl font-black text-brand-600 dark:text-brand-400">
            {report.final_score}
          </span>
          <span className="text-xs text-slate-400 font-semibold uppercase mt-0.5">out of 100</span>
          <div className="mt-2.5 px-3 py-1 rounded-full text-[11px] font-bold bg-white dark:bg-slate-900 shadow-sm text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700">
            {report.performance_band}
          </div>
        </div>
      </div>

      {/* Dimension Breakdown Chart */}
      <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <BarChart2 className="w-4 h-4 text-brand-500" />
            Evaluation Dimensions Breakdown (Scale 0 - 10)
          </h2>
          <span className="text-xs text-slate-400">Weighted Average Marks</span>
        </div>

        <div className="h-64 w-full pt-4">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
              <XAxis dataKey="name" tick={{ fontSize: 11 }} interval={0} stroke="#94a3b8" />
              <YAxis domain={[0, 10]} ticks={[0, 2, 4, 6, 8, 10]} tick={{ fontSize: 11 }} stroke="#94a3b8" />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="p-2.5 rounded-xl bg-slate-900 text-white text-xs shadow-lg space-y-0.5">
                        <div className="font-bold">{data.name}</div>
                        <div>Mark: {data.score} / 10 ({data.percentage}%)</div>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Bar dataKey="score" radius={[6, 6, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={getScoreColor(entry.percentage)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Strengths & Areas to Improve Grid */}
      <div className="grid sm:grid-cols-2 gap-6">
        {/* Strengths */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
          <h3 className="text-sm font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            Key Demonstrated Strengths
          </h3>
          <ul className="space-y-2 text-xs text-slate-600 dark:text-slate-300">
            {report.strengths.map((str, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-1.5 shrink-0"></span>
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Improvement Areas */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
          <h3 className="text-sm font-bold text-amber-600 dark:text-amber-400 flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            Target Improvement Areas
          </h3>
          <ul className="space-y-2 text-xs text-slate-600 dark:text-slate-300">
            {report.areas_for_improvement.map((area, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5 shrink-0"></span>
                <span>{area}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Practice Recommendations */}
      <div className="p-6 rounded-3xl bg-brand-50/50 dark:bg-slate-900/80 border border-brand-200 dark:border-slate-800 space-y-3 shadow-sm">
        <h3 className="text-sm font-bold text-brand-700 dark:text-brand-300 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-brand-500" />
          Recommended Next Steps for Placement
        </h3>
        <div className="grid sm:grid-cols-2 gap-3 text-xs">
          {report.practice_recommendations.map((rec, idx) => (
            <div
              key={idx}
              className="p-3 rounded-xl bg-white dark:bg-slate-800/80 border border-brand-100 dark:border-slate-700 text-slate-700 dark:text-slate-300 flex items-start gap-2"
            >
              <div className="w-5 h-5 rounded-md bg-brand-100 dark:bg-brand-900/60 text-brand-600 dark:text-brand-400 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">
                {idx + 1}
              </div>
              <span>{rec}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Turn-by-Turn Transcripts */}
      <div className="space-y-4">
        <h2 className="text-base font-bold text-slate-900 dark:text-white">
          Turn-by-Turn Answer Transcripts
        </h2>

        <div className="space-y-4">
          {report.turns.map((turn) => {
            const ev = turn.evaluation;
            return (
              <div
                key={turn.id}
                className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4 text-xs shadow-sm"
              >
                <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
                  <span className="font-bold text-slate-900 dark:text-white">
                    Question #{turn.sequence}: {turn.question_text}
                  </span>
                  <span className="font-bold px-2.5 py-1 rounded-full bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400 text-xs">
                    Mark: {turn.overall_score}/100
                  </span>
                </div>

                <div className="space-y-1">
                  <span className="text-[10px] font-bold uppercase text-slate-400">
                    Your Submitted Answer:
                  </span>
                  <p className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50 text-slate-700 dark:text-slate-300 italic">
                    "{turn.answer_text}"
                  </p>
                </div>

                {ev?.ideal_answer && (
                  <div className="space-y-1">
                    <span className="text-[10px] font-bold uppercase text-emerald-600 dark:text-emerald-400">
                      Ideal Reference Concept:
                    </span>
                    <p className="p-3 rounded-xl bg-emerald-50/40 dark:bg-emerald-950/20 text-slate-700 dark:text-slate-300">
                      {ev.ideal_answer}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Footer Navigation Buttons */}
      <div className="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-slate-200 dark:border-slate-800">
        <Link
          to="/dashboard"
          className="px-5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 text-xs font-semibold hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        >
          Return to Dashboard
        </Link>
        <Link
          to="/interview/new"
          className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs shadow-md transition-all hover:scale-105"
        >
          Practice Another Round
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
};
