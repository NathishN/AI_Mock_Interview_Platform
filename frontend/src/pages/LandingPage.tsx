import React from 'react';
import { Link } from 'react-router-dom';
import {
  Sparkles,
  BookOpen,
  Mic,
  MessageSquare,
  Building2,
  TrendingUp,
  Award,
  CheckCircle2,
  ArrowRight,
  ShieldCheck,
  Zap,
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  return (
    <div className="space-y-24 py-8">
      {/* Hero Section */}
      <section className="text-center max-w-4xl mx-auto space-y-6 pt-8">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400 border border-brand-200 dark:border-brand-800 shadow-sm">
          <Sparkles className="w-3.5 h-3.5" />
          Powered by Groq Ultra-Low Latency Inference
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-slate-900 dark:text-white leading-[1.15]">
          Crack Campus Placements with <span className="bg-gradient-to-r from-brand-600 to-indigo-500 bg-clip-text text-transparent">InterviewAce AI</span>
        </h1>

        <p className="text-base sm:text-lg text-slate-600 dark:text-slate-300 max-w-2xl mx-auto font-normal">
          The comprehensive interview preparation SaaS built specifically for Indian engineering students and freshers. Practice real technical rounds, master HR questions, and receive objective rubric scoring.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-4">
          <Link
            to="/register"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-semibold shadow-md shadow-brand-500/20 transition-all text-sm"
          >
            Start Free Practice
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            to="/library"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-800 dark:text-slate-200 font-semibold transition-all text-sm"
          >
            <BookOpen className="w-4 h-4 text-brand-500" />
            Explore 500 Questions
          </Link>
        </div>

        {/* Quick Highlights Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-12 border-t border-slate-200 dark:border-slate-800">
          <div>
            <div className="text-2xl font-bold text-slate-900 dark:text-white">500</div>
            <div className="text-xs text-slate-500 dark:text-slate-400 font-medium">Curated Questions</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-900 dark:text-white">100/100</div>
            <div className="text-xs text-slate-500 dark:text-slate-400 font-medium">Deterministic Rubric Marks</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-900 dark:text-white">5</div>
            <div className="text-xs text-slate-500 dark:text-slate-400 font-medium">Interview Presets</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-900 dark:text-white">&lt; 1s</div>
            <div className="text-xs text-slate-500 dark:text-slate-400 font-medium">Groq AI Evaluation</div>
          </div>
        </div>
      </section>

      {/* Pillars Section */}
      <section className="space-y-12">
        <div className="text-center max-w-xl mx-auto space-y-2">
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white">
            Deliberate Practice for Every Interview Stage
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            From technical screening and coding to HR and managerial discussions.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Card 1 */}
          <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm hover:border-brand-500/50 transition-colors space-y-4">
            <div className="w-10 h-10 rounded-xl bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400 flex items-center justify-center font-bold">
              <Mic className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900 dark:text-white">
              AI Mock Interview Room
            </h3>
            <p className="text-xs leading-relaxed text-slate-600 dark:text-slate-400">
              Simulates realistic interview conditions with speech and text input. Questions adapt in real-time based on candidate performance.
            </p>
          </div>

          {/* Card 2 */}
          <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm hover:border-brand-500/50 transition-colors space-y-4">
            <div className="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center font-bold">
              <MessageSquare className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900 dark:text-white">
              HR Answer Improvement Studio
            </h3>
            <p className="text-xs leading-relaxed text-slate-600 dark:text-slate-400">
              Build personalized, authentic answers for "Tell me about yourself", strengths, and weaknesses without hallucinating personal details.
            </p>
          </div>

          {/* Card 3 */}
          <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm hover:border-brand-500/50 transition-colors space-y-4">
            <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center font-bold">
              <Building2 className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900 dark:text-white">
              Company-Specific Guides
            </h3>
            <p className="text-xs leading-relaxed text-slate-600 dark:text-slate-400">
              Round-by-round hiring breakdowns and coaching tips for TCS, Infosys, Amazon, Google, Accenture, and other campus recruiters.
            </p>
          </div>

          {/* Card 4 */}
          <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm hover:border-brand-500/50 transition-colors space-y-4">
            <div className="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400 flex items-center justify-center font-bold">
              <Award className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900 dark:text-white">
              Deterministic Scoring Engine
            </h3>
            <p className="text-xs leading-relaxed text-slate-600 dark:text-slate-400">
              Marks scored 0-10 across technical correctness, clarity, completeness, and reasoning, scaled reliably to a 100-point total.
            </p>
          </div>

          {/* Card 5 */}
          <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm hover:border-brand-500/50 transition-colors space-y-4">
            <div className="w-10 h-10 rounded-xl bg-rose-50 dark:bg-rose-950/60 text-rose-600 dark:text-rose-400 flex items-center justify-center font-bold">
              <TrendingUp className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900 dark:text-white">
              Progress & Readiness Analytics
            </h3>
            <p className="text-xs leading-relaxed text-slate-600 dark:text-slate-400">
              Track skill breakdowns on radar charts, monitor score trends over time, and remediate recurring weak areas.
            </p>
          </div>

          {/* Card 6 */}
          <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm hover:border-brand-500/50 transition-colors space-y-4">
            <div className="w-10 h-10 rounded-xl bg-cyan-50 dark:bg-cyan-950/60 text-cyan-600 dark:text-cyan-400 flex items-center justify-center font-bold">
              <BookOpen className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900 dark:text-white">
              500 Knowledge Base Library
            </h3>
            <p className="text-xs leading-relaxed text-slate-600 dark:text-slate-400">
              Exhaustive collection across HR, Behavioral, Python, SQL, ML/AI, System Projects, and Coding with model answers and common mistakes.
            </p>
          </div>
        </div>
      </section>

      {/* Call to action */}
      <section className="p-8 sm:p-12 rounded-3xl bg-gradient-to-tr from-brand-900 to-indigo-900 text-white text-center space-y-6 shadow-xl">
        <h2 className="text-2xl sm:text-4xl font-extrabold tracking-tight text-white">
          Ready to Clear Your Dream Company Interview?
        </h2>
        <p className="text-sm sm:text-base text-slate-300 max-w-xl mx-auto">
          Join thousands of engineering freshers mastering high-pressure interviews through objective, AI-driven coaching.
        </p>
        <div>
          <Link
            to="/register"
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-white text-brand-900 hover:bg-slate-100 font-bold text-sm shadow-lg transition-transform hover:scale-105"
          >
            Create Free Account
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>
    </div>
  );
};
