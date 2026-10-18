import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Building2,
  Sparkles,
  Clock,
  CheckCircle,
  ArrowRight,
  BookOpen,
  Mic,
  ChevronRight,
} from 'lucide-react';
import { companyPrepApi, CompanyGuide } from '../api/companyPrep';

export const CompanyPrepPage: React.FC = () => {
  const { slug } = useParams<{ slug?: string }>();
  const [companies, setCompanies] = useState<CompanyGuide[]>([]);
  const [selectedCompany, setSelectedCompany] = useState<CompanyGuide | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    companyPrepApi
      .listCompanies()
      .then((data) => {
        setCompanies(data);
        if (data.length > 0) {
          const match = slug
            ? data.find((c) => c.slug.toLowerCase() === slug.toLowerCase())
            : data[0];
          setSelectedCompany(match || data[0]);
        }
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) {
    return (
      <div className="py-24 text-center text-xs text-slate-500">
        <div className="w-7 h-7 border-3 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
        Loading Company Placement Guides...
      </div>
    );
  }

  return (
    <div className="space-y-6 py-4">
      {/* Header */}
      <div className="space-y-1.5">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400">
          <Building2 className="w-3.5 h-3.5" />
          Campus Hiring Pipelines
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
          Company-Specific Preparation Guides
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 max-w-2xl">
          Detailed round-by-round breakdown, syllabus focus areas, and insider placement tips for major Indian tech recruiters.
        </p>
      </div>

      {/* Main Container */}
      <div className="grid lg:grid-cols-4 gap-6">
        {/* Company Selector Sidebar */}
        <div className="space-y-2">
          <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider px-1">
            Top Tech Recruiters
          </h2>
          <div className="space-y-1.5">
            {companies.map((comp) => {
              const isSelected = selectedCompany?.id === comp.id;
              return (
                <button
                  key={comp.id}
                  onClick={() => setSelectedCompany(comp)}
                  className={`w-full text-left p-3 rounded-2xl border transition-all flex items-center justify-between ${
                    isSelected
                      ? 'border-brand-500 bg-brand-50/50 dark:bg-brand-950/40 shadow-sm'
                      : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white font-bold flex items-center justify-center text-xs">
                      {comp.logo_letter}
                    </div>
                    <div>
                      <div className="text-xs font-bold text-slate-900 dark:text-white">
                        {comp.name}
                      </div>
                      <div className="text-[10px] text-slate-400">{comp.category}</div>
                    </div>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-400" />
                </button>
              );
            })}
          </div>
        </div>

        {/* Selected Company Guide (3 Columns) */}
        {selectedCompany && (
          <div className="lg:col-span-3 space-y-6">
            {/* Overview Card */}
            <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-2xl bg-brand-600 text-white font-black text-xl flex items-center justify-center shadow-md">
                    {selectedCompany.logo_letter}
                  </div>
                  <div>
                    <h2 className="text-lg sm:text-xl font-bold text-slate-900 dark:text-white">
                      {selectedCompany.name}
                    </h2>
                    <span className="text-xs text-slate-500 dark:text-slate-400">
                      {selectedCompany.category} • {selectedCompany.hiring_rounds} Hiring Rounds • Difficulty: {selectedCompany.difficulty}
                    </span>
                  </div>
                </div>

                <Link
                  to="/interview/new"
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs shadow-md transition-all hover:scale-105"
                >
                  <Mic className="w-3.5 h-3.5" />
                  Mock Interview for {selectedCompany.name}
                </Link>
              </div>

              <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                {selectedCompany.description}
              </p>
            </div>

            {/* Rounds Pipeline */}
            <div className="space-y-3">
              <h3 className="text-sm font-bold text-slate-900 dark:text-white">
                Round-by-Round Selection Pipeline
              </h3>

              <div className="space-y-3">
                {selectedCompany.rounds.map((round) => (
                  <div
                    key={round.round_number}
                    className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3 text-xs"
                  >
                    <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-2">
                      <span className="font-bold text-slate-900 dark:text-white flex items-center gap-2">
                        <span className="w-5 h-5 rounded-md bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400 text-[10px] font-bold flex items-center justify-center">
                          {round.round_number}
                        </span>
                        {round.name} ({round.stage})
                      </span>
                      <span className="text-slate-400 flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5" /> {round.duration_minutes} mins
                      </span>
                    </div>

                    <p className="text-slate-600 dark:text-slate-300 leading-relaxed">
                      {round.description}
                    </p>

                    <div className="flex flex-wrap items-center gap-1.5 pt-1">
                      <span className="text-[11px] font-semibold text-slate-400 mr-1">
                        Focus Areas:
                      </span>
                      {round.focus_areas.map((f, i) => (
                        <span
                          key={i}
                          className="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300"
                        >
                          {f}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Insider Placement Tips */}
            <div className="p-6 rounded-3xl bg-amber-50/40 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/40 space-y-3">
              <h3 className="text-xs font-bold text-amber-800 dark:text-amber-300 uppercase tracking-wider flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-amber-500" />
                Insider Placement Strategy & Tips
              </h3>
              <ul className="space-y-2 text-xs text-slate-700 dark:text-slate-300">
                {selectedCompany.key_tips.map((tip, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <CheckCircle className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400 mt-0.5 shrink-0" />
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Recommended Question Categories */}
            <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="space-y-1">
                <span className="text-xs font-bold text-slate-900 dark:text-white">
                  Targeted Questions in the 500 Knowledge Base
                </span>
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {selectedCompany.recommended_question_categories.map((cat, i) => (
                    <span
                      key={i}
                      className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400"
                    >
                      {cat}
                    </span>
                  ))}
                </div>
              </div>

              <Link
                to={`/library?category=${selectedCompany.recommended_question_categories[0]}`}
                className="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-xs font-semibold text-slate-800 dark:text-slate-200 flex items-center gap-1.5 transition-colors shrink-0"
              >
                <BookOpen className="w-3.5 h-3.5" />
                Explore Related Questions
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
