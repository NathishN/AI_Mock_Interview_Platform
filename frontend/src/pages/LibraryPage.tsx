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
  Calculator,
  Compass,
  Sparkles,
} from 'lucide-react';
import { questionsApi, Question } from '../api/questions';

const CATEGORIES = [
  'All',
  'Aptitude',
  'Coding',
  'SQL & Analytics',
  'Operating Systems',
  'ML, AI & GenAI',
  'Resume & Projects',
  'HR',
  'Behavioral',
  'Python',
  'Java & OOP',
  'Web Development',
  'Git & CI/CD',
  'Networking & IoT',
  'Company & Workplace',
];

const DIFFICULTIES = ['All', 'Beginner', 'Intermediate', 'Advanced'];

const QUICK_TAG_FILTERS = [
  { id: 'all', label: 'All Curated Questions' },
  { id: 'aptitude', label: '🧮 Aptitude & Quant (150)' },
  { id: 'top-30', label: '⭐ Top 30 High Priority' },
  { id: 'master-bank', label: '🏢 Master Bank' },
  { id: 'ibm', label: 'IBM' },
  { id: 'hexaware', label: 'Hexaware' },
  { id: 'payoda', label: 'Payoda' },
  { id: 'sws-ai', label: 'SWS AI' },
  { id: 'aquaairx', label: 'AquaAirX' },
  { id: 'wheelson', label: 'Wheelson' },
];

export const LibraryPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialCategory = searchParams.get('category') || 'All';
  const initialDifficulty = searchParams.get('difficulty') || 'All';
  const initialTag = searchParams.get('tag') || 'all';
  const initialSearch = searchParams.get('q') || '';

  const [category, setCategory] = useState(initialCategory);
  const [difficulty, setDifficulty] = useState(initialDifficulty);
  const [activeTag, setActiveTag] = useState(initialTag);
  const [searchTerm, setSearchTerm] = useState(initialSearch);

  const [questions, setQuestions] = useState<Question[]>([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showAptitudeCheatSheet, setShowAptitudeCheatSheet] = useState(false);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      setError(null);
      const params: Record<string, any> = { limit: 100 };
      if (category !== 'All') params.category = category;
      if (difficulty !== 'All') params.difficulty = difficulty;
      if (activeTag !== 'all') params.tag = activeTag;
      if (searchTerm.trim()) params.search = searchTerm.trim();

      const res = await questionsApi.list(params);
      setQuestions(res.items);
      setTotalCount(res.total);
    } catch (err: any) {
      console.error(err);
      if (err?.response?.status === 401) {
        setError('Authentication required to access the Question Bank. Please log in.');
      } else {
        setError('Unable to load questions. Please check your connection and retry.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, [category, difficulty, activeTag]);

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
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-50 dark:bg-brand-950/60 border border-brand-200 dark:border-brand-800 text-brand-700 dark:text-brand-300 text-xs font-semibold">
          <span>⚡ Master Interview Question Bank</span>
          <span>•</span>
          <span>{totalCount} Questions Active</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white flex items-center gap-2.5">
          <BookOpen className="w-7 h-7 text-brand-600" />
          Master Interview Question Bank & Knowledge Base
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 max-w-3xl leading-relaxed">
          Consolidated technical and HR question bank from real interview experiences at{' '}
          <strong className="text-slate-900 dark:text-white">IBM, Hexaware, Payoda, SWS AI, AquaAirX, and Wheelson Technologies</strong>.
          Study model answers, key evaluation criteria, common mistakes, and practice live in the mock room.
        </p>
      </div>

      {/* Quick Company & Priority Tag Filters */}
      <div className="p-3.5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-2 shadow-sm">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
            <Tag className="w-3.5 h-3.5 text-brand-500" />
            Curated Company & Priority Tracks:
          </span>
          {activeTag !== 'all' && (
            <button
              onClick={() => setActiveTag('all')}
              className="text-[11px] text-brand-600 hover:underline font-semibold"
            >
              Reset Filter
            </button>
          )}
        </div>
        <div className="flex flex-wrap gap-1.5">
          {QUICK_TAG_FILTERS.map((tf) => {
            const isSelected = activeTag === tf.id;
            return (
              <button
                key={tf.id}
                onClick={() => setActiveTag(tf.id)}
                className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                  isSelected
                    ? 'bg-brand-600 text-white shadow-sm'
                    : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
                }`}
              >
                {tf.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Aptitude 150 Formulas & Strategy Action Banner */}
      <div className="rounded-2xl border border-indigo-200 dark:border-indigo-900/60 bg-gradient-to-r from-indigo-50/70 via-purple-50/50 to-brand-50/60 dark:from-indigo-950/40 dark:via-purple-950/20 dark:to-brand-950/30 p-4 shadow-sm transition-all">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div className="space-y-1">
            <div className="inline-flex items-center gap-1.5 text-xs font-bold text-indigo-700 dark:text-indigo-400">
              <Calculator className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
              <span>Campus Placement Aptitude Master Track</span>
              <span className="text-slate-400">•</span>
              <span className="px-1.5 py-0.5 rounded bg-indigo-100 dark:bg-indigo-900/60 text-[10px] font-extrabold uppercase">150 Questions</span>
            </div>
            <p className="text-xs text-slate-600 dark:text-slate-300">
              Quantitative Aptitude, Logical Reasoning, Verbal Ability & Data Interpretation with step-by-step solutions and speed-math tricks.
            </p>
          </div>
          <div className="flex items-center gap-2 w-full sm:w-auto">
            <button
              onClick={() => {
                setCategory('Aptitude');
                setActiveTag('all');
              }}
              className="flex-1 sm:flex-none px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs shadow-sm transition-all text-center"
            >
              Filter Aptitude Questions
            </button>
            <button
              onClick={() => setShowAptitudeCheatSheet((prev) => !prev)}
              className="px-3.5 py-2 rounded-xl border border-indigo-300 dark:border-indigo-800 bg-white dark:bg-slate-900 hover:bg-indigo-50 dark:hover:bg-slate-800 text-indigo-700 dark:text-indigo-300 font-semibold text-xs transition-colors flex items-center gap-1.5"
            >
              <Compass className="w-3.5 h-3.5" />
              {showAptitudeCheatSheet ? 'Hide Cheat Sheet' : 'Formula & Crash Plan'}
            </button>
          </div>
        </div>

        {/* Collapsible Formulas & Strategies Sheet */}
        {showAptitudeCheatSheet && (
          <div className="mt-4 pt-4 border-t border-indigo-100 dark:border-indigo-900/40 space-y-4 text-xs">
            {/* The 20 Formulas Grid */}
            <div className="space-y-2">
              <h4 className="font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
                <Sparkles className="w-4 h-4 text-amber-500" />
                The 20 Must-Memorize Aptitude Formulas:
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
                {[
                  { topic: 'Percentage', formula: '(Part / Whole) × 100' },
                  { topic: 'Profit %', formula: '(Profit / CP) × 100' },
                  { topic: 'Loss %', formula: '(Loss / CP) × 100' },
                  { topic: 'Discount %', formula: '[(MP − SP) / MP] × 100' },
                  { topic: 'Average', formula: 'Sum of Terms / Total Count' },
                  { topic: 'Speed', formula: 'Distance / Time' },
                  { topic: 'Relative Speed', formula: 'Same Dir: S1 − S2 | Opp: S1 + S2' },
                  { topic: 'Speed Conversion', formula: 'km/h × (5/18) = m/s' },
                  { topic: 'Time & Work', formula: 'If A takes N days, 1-day work = 1/N' },
                  { topic: 'Together Work', formula: '(A × B) / (A + B) days' },
                  { topic: 'Simple Interest', formula: '(P × R × T) / 100' },
                  { topic: 'Compound Interest', formula: 'P(1 + R/100)^T − P' },
                  { topic: 'CI − SI (2 Years)', formula: 'P × (R / 100)²' },
                  { topic: 'Successive %', formula: 'a + b + (ab / 100)%' },
                  { topic: 'Equal +/- Change', formula: '+x% & −x% = (x²/100)% Net Loss' },
                  { topic: 'Ranking Total', formula: 'Total = Top + Bottom − 1' },
                  { topic: 'Circular Opposite', formula: 'Between = (N − 2) / 2' },
                  { topic: 'Probability', formula: 'Favorable Cases / Total Cases' },
                  { topic: 'Permutation', formula: 'nPr = n! / (n − r)!' },
                  { topic: 'Combination', formula: 'nCr = n! / [r!(n − r)!]' },
                ].map((item, idx) => (
                  <div key={idx} className="p-2.5 rounded-xl bg-white dark:bg-slate-900 border border-indigo-100 dark:border-indigo-950 flex flex-col justify-between">
                    <span className="font-semibold text-slate-500 dark:text-slate-400 text-[11px]">{item.topic}</span>
                    <span className="font-mono font-bold text-slate-900 dark:text-white mt-1 text-[11px]">{item.formula}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Exam Hall Rules and Crash Plan */}
            <div className="grid sm:grid-cols-2 gap-3 pt-1">
              <div className="p-3 rounded-xl bg-white dark:bg-slate-900 border border-indigo-100 dark:border-indigo-950 space-y-1.5">
                <span className="font-bold text-slate-900 dark:text-white text-xs flex items-center gap-1.5">
                  ⚡ 5 Golden Exam-Hall Rules:
                </span>
                <ul className="text-slate-600 dark:text-slate-400 space-y-1 text-[11px] list-disc list-inside">
                  <li><strong>30–45s Rule:</strong> If no clear path in 45 seconds, flag and skip immediately.</li>
                  <li><strong>Accuracy First:</strong> Target high accuracy over blind volume to beat negative marking.</li>
                  <li><strong>Percentage Trap:</strong> +20% followed by −20% is NOT 0% (it is a 4% decrease).</li>
                  <li><strong>Speed Anchors:</strong> 36 km/h = 10 m/s; 72 km/h = 20 m/s; 108 km/h = 30 m/s.</li>
                  <li><strong>Ranking -1:</strong> Always subtract 1 when summing top and bottom rank of a person.</li>
                </ul>
              </div>

              <div className="p-3 rounded-xl bg-white dark:bg-slate-900 border border-indigo-100 dark:border-indigo-950 space-y-1.5">
                <span className="font-bold text-slate-900 dark:text-white text-xs flex items-center gap-1.5">
                  🔥 12-Hour Placement Crash Plan:
                </span>
                <ul className="text-slate-600 dark:text-slate-400 space-y-1 text-[11px] list-disc list-inside">
                  <li><strong>Hours 1–2:</strong> Percentages, Profit/Loss, Ratios, Averages, Time & Work.</li>
                  <li><strong>Hours 3–4:</strong> Speed/Distance, Number Series, Coding-Decoding, Blood Relations.</li>
                  <li><strong>Hours 5–6:</strong> Direction Sense, Syllogisms, Seating Arrangement & Ranking.</li>
                  <li><strong>Hour 7:</strong> Verbal Ability: Grammar, Prepositions, Sentence Corrections.</li>
                  <li><strong>Hour 8:</strong> Data Interpretation Table calculations & shortcuts.</li>
                  <li><strong>Final 2 Hours:</strong> Timed practice with mock tests.</li>
                </ul>
              </div>
            </div>
          </div>
        )}
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
      ) : error ? (
        <div className="p-8 text-center bg-white dark:bg-slate-900 rounded-2xl border border-rose-200 dark:border-rose-900/40 text-xs text-rose-600 dark:text-rose-400 space-y-3">
          <p className="font-medium">{error}</p>
          <div className="flex items-center justify-center gap-3">
            <button
              onClick={() => fetchQuestions()}
              className="px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-semibold text-xs transition-colors"
            >
              Retry
            </button>
            <Link
              to="/login"
              className="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 font-semibold text-xs hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
            >
              Go to Login
            </Link>
          </div>
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
                      {q.tags && q.tags.includes('top-30') && (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border border-amber-300 dark:border-amber-800">
                          ⭐ Top 30 Priority
                        </span>
                      )}
                      {q.tags && q.tags.includes('master-bank') && (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-900">
                          Master Bank
                        </span>
                      )}
                      {q.tags &&
                        q.tags
                          .filter((t) =>
                            ['ibm', 'hexaware', 'payoda', 'sws-ai', 'aquaairx', 'wheelson'].includes(
                              t.toLowerCase()
                            )
                          )
                          .map((ct, idx) => (
                            <span
                              key={idx}
                              className="px-1.5 py-0.5 rounded text-[9px] font-extrabold uppercase bg-purple-50 dark:bg-purple-950/60 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-800"
                            >
                              {ct}
                            </span>
                          ))}
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
