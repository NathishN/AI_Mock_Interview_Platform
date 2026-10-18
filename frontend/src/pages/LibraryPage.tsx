import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import {
  Search,
  Filter,
  BookOpen,
  ChevronDown,
  ChevronUp,
  Tag,
  AlertTriangle,
  CheckCircle,
  HelpCircle,
  Mic,
  Code2,
} from 'lucide-react';
import { questionsApi, Question } from '../api/questions';

const CATEGORIES = [
  'All',
  'HR',
  'Behavioral',
  'Resume & Projects',
  'Python',
  'SQL & Analytics',
  'ML, AI & GenAI',
  'Company & Workplace',
  'Coding',
];

const DIFFICULTIES = ['All', 'Beginner', 'Intermediate', 'Advanced'];

export const LibraryPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialCategory = searchParams.get('category') || 'All';
  const initialDifficulty = searchParams.get('difficulty') || 'All';
  const initialSearch = searchParams.get('q') || '';

  const [category, setCategory] = useState(initialCategory);
  const [difficulty, setDifficulty] = useState(initialDifficulty);
  const [searchTerm, setSearchTerm] = useState(initialSearch);

  const [questions, setQuestions] = useState<Question[]>([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      const params: Record<string, any> = { limit: 100 };
      if (category !== 'All') params.category = category;
      if (difficulty !== 'All') params.difficulty = difficulty;
      if (searchTerm.trim()) params.search = searchTerm.trim();

      const res = await questionsApi.list(params);
      setQuestions(res.items);
      setTotalCount(res.total);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, [category, difficulty]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchQuestions();
  };

  const toggleExpand = (id: string) => {
    setExpandedId((prev) => (prev === id ? null : id));
  };

  return (
    <div className="space-y-6 py-4">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white flex items-center gap-2.5">
          <BookOpen className="w-6 h-6 text-brand-600" />
          500-Question Knowledge Base
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
          Curated interview questions frequently encountered in Indian campus placements and entry-level engineering interviews.
        </p>
      </div>

      {/* Search and Filters Bar */}
      <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
        <form onSubmit={handleSearchSubmit} className="flex gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search across questions, topics, algorithms, or keywords..."
              className="w-full pl-9 pr-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-semibold text-xs transition-colors"
          >
            Search
          </button>
        </form>

        {/* Categories Pills */}
        <div className="flex flex-wrap gap-1.5 items-center">
          <span className="text-xs font-semibold text-slate-500 mr-1 flex items-center gap-1">
            <Filter className="w-3.5 h-3.5" /> Category:
          </span>
          {CATEGORIES.map((cat) => {
            const isSelected = category === cat;
            return (
              <button
                key={cat}
                onClick={() => setCategory(cat)}
                className={`px-2.5 py-1 rounded-lg text-xs font-medium border transition-colors ${
                  isSelected
                    ? 'bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400 border-brand-300 dark:border-brand-800'
                    : 'border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800'
                }`}
              >
                {cat}
              </button>
            );
          })}
        </div>

        {/* Difficulty Selector */}
        <div className="flex items-center gap-2 pt-1">
          <span className="text-xs font-semibold text-slate-500">Difficulty:</span>
          {DIFFICULTIES.map((diff) => (
            <button
              key={diff}
              onClick={() => setDifficulty(diff)}
              className={`px-2 py-0.5 rounded text-[11px] font-semibold border ${
                difficulty === diff
                  ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 border-transparent'
                  : 'text-slate-500 dark:text-slate-400 border-slate-200 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
            >
              {diff}
            </button>
          ))}
          <span className="ml-auto text-xs font-medium text-slate-400">
            Showing {questions.length} of {totalCount} records
          </span>
        </div>
      </div>

      {/* Questions List */}
      {loading ? (
        <div className="py-16 text-center text-xs text-slate-500">
          <div className="w-6 h-6 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
          Loading questions...
        </div>
      ) : questions.length === 0 ? (
        <div className="p-8 text-center bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 text-xs text-slate-500">
          No questions matched your filter criteria. Try adjusting the search term or category.
        </div>
      ) : (
        <div className="space-y-3">
          {questions.map((q) => {
            const isExpanded = expandedId === q.id;
            return (
              <div
                key={q.id}
                className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 overflow-hidden shadow-sm transition-all"
              >
                {/* Question Row Header */}
                <div
                  onClick={() => toggleExpand(q.id)}
                  className="p-4 sm:p-5 flex items-start justify-between gap-4 cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800/40 select-none"
                >
                  <div className="space-y-2 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="font-mono text-[10px] text-slate-400 font-bold uppercase">
                        {q.id}
                      </span>
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400">
                        {q.category}
                      </span>
                      {q.subcategory && (
                        <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                          {q.subcategory}
                        </span>
                      )}
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                          q.difficulty === 'Beginner'
                            ? 'text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40'
                            : q.difficulty === 'Intermediate'
                            ? 'text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/40'
                            : 'text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-950/40'
                        }`}
                      >
                        {q.difficulty}
                      </span>
                    </div>

                    <h3 className="text-sm sm:text-base font-semibold text-slate-900 dark:text-white leading-snug">
                      {q.question}
                    </h3>
                  </div>

                  <div className="flex items-center gap-2 shrink-0 pt-1">
                    <button
                      className="p-1 rounded text-slate-400 hover:text-slate-700 dark:hover:text-slate-200"
                      aria-label="Expand details"
                    >
                      {isExpanded ? (
                        <ChevronUp className="w-5 h-5" />
                      ) : (
                        <ChevronDown className="w-5 h-5" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Expanded Details */}
                {isExpanded && (
                  <div className="p-5 border-t border-slate-100 dark:border-slate-800/80 bg-slate-50/50 dark:bg-slate-950/50 space-y-6 text-xs">
                    {/* Model Reference Answer */}
                    <div className="space-y-1.5">
                      <div className="font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
                        <CheckCircle className="w-4 h-4 text-emerald-500" />
                        Model Reference Answer & Framework
                      </div>
                      <div className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-wrap font-sans">
                        {q.reference_answer}
                      </div>
                    </div>

                    {/* Key Evaluation Points & Criteria */}
                    <div className="grid sm:grid-cols-2 gap-4">
                      <div className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-2">
                        <div className="font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
                          <CheckCircle className="w-3.5 h-3.5 text-brand-500" />
                          Key Points to Cover
                        </div>
                        <ul className="space-y-1 text-slate-600 dark:text-slate-400 list-disc list-inside">
                          {q.key_points.map((pt, i) => (
                            <li key={i}>{pt}</li>
                          ))}
                        </ul>
                      </div>

                      <div className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-2">
                        <div className="font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
                          <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
                          Common Candidate Mistakes
                        </div>
                        <ul className="space-y-1 text-slate-600 dark:text-slate-400 list-disc list-inside">
                          {q.common_mistakes.map((cm, i) => (
                            <li key={i}>{cm}</li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    {/* Follow-up Questions if any */}
                    {q.follow_up_questions && q.follow_up_questions.length > 0 && (
                      <div className="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-2">
                        <div className="font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
                          <HelpCircle className="w-3.5 h-3.5 text-indigo-500" />
                          Anticipated Follow-Up Questions
                        </div>
                        <ul className="space-y-1 text-slate-600 dark:text-slate-400 list-disc list-inside">
                          {q.follow_up_questions.map((fu, i) => (
                            <li key={i}>{fu}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Tags & Action */}
                    <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
                      <div className="flex flex-wrap gap-1">
                        {q.tags.map((tag, i) => (
                          <span
                            key={i}
                            className="text-[10px] font-medium text-slate-500 dark:text-slate-400 bg-slate-200/60 dark:bg-slate-800 px-2 py-0.5 rounded"
                          >
                            #{tag}
                          </span>
                        ))}
                      </div>

                      <Link
                        to="/interview/new"
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-brand-600 hover:bg-brand-700 text-white font-semibold text-xs transition-colors"
                      >
                        <Mic className="w-3.5 h-3.5" />
                        Practice Live in Mock Room
                      </Link>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
