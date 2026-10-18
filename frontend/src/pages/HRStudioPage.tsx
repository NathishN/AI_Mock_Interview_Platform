import React, { useState, useEffect } from 'react';
import {
  MessageSquare,
  Sparkles,
  CheckCircle,
  AlertTriangle,
  Save,
  Trash2,
  Send,
  HelpCircle,
  Layers,
  Wand2,
} from 'lucide-react';
import {
  hrStudioApi,
  HRTopic,
  HRDraft,
  HRAnalysisResult,
} from '../api/hrStudio';

export const HRStudioPage: React.FC = () => {
  const [topics, setTopics] = useState<HRTopic[]>([]);
  const [selectedTopicId, setSelectedTopicId] = useState<string>('self_introduction');
  const [activeTab, setActiveTab] = useState<'builder' | 'critique'>('builder');

  // Fact-to-answer builder state
  const [facts, setFacts] = useState<Record<string, string>>({});
  const [generatedAnswer, setGeneratedAnswer] = useState<string>('');
  const [finalAnswer, setFinalAnswer] = useState<string>('');
  const [generating, setGenerating] = useState<boolean>(false);
  const [saving, setSaving] = useState<boolean>(false);

  // Critique state
  const [critiqueInput, setCritiqueInput] = useState<string>('');
  const [analysis, setAnalysis] = useState<HRAnalysisResult | null>(null);
  const [analyzing, setAnalyzing] = useState<boolean>(false);

  // Saved drafts
  const [drafts, setDrafts] = useState<HRDraft[]>([]);

  useEffect(() => {
    hrStudioApi
      .getTopics()
      .then((data) => {
        setTopics(data);
        if (data.length > 0) setSelectedTopicId(data[0].id);
      })
      .catch((err) => console.error(err));

    loadDrafts();
  }, []);

  const loadDrafts = async () => {
    try {
      const d = await hrStudioApi.listDrafts();
      setDrafts(d);
    } catch (err) {
      console.error(err);
    }
  };

  const currentTopic = topics.find((t) => t.id === selectedTopicId);

  const handleFactChange = (key: string, val: string) => {
    setFacts((prev) => ({ ...prev, [key]: val }));
  };

  const handleGenerate = async () => {
    try {
      setGenerating(true);
      const res = await hrStudioApi.generateAnswer(selectedTopicId, facts);
      setGeneratedAnswer(res.generated_answer);
      setFinalAnswer(res.generated_answer);
      setCritiqueInput(res.generated_answer);
    } catch (err) {
      console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  const handleSaveDraft = async () => {
    if (!finalAnswer.trim()) return;
    try {
      setSaving(true);
      await hrStudioApi.saveDraft({
        topic: selectedTopicId,
        facts,
        generated_answer: generatedAnswer,
        final_answer: finalAnswer,
      });
      await loadDrafts();
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteDraft = async (id: string) => {
    try {
      await hrStudioApi.deleteDraft(id);
      setDrafts((prev) => prev.filter((d) => d.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  const handleAnalyzeDraft = async () => {
    if (!critiqueInput.trim()) return;
    try {
      setAnalyzing(true);
      const result = await hrStudioApi.analyzeDraft(selectedTopicId, critiqueInput.trim());
      setAnalysis(result);
    } catch (err) {
      console.error(err);
    } finally {
      setAnalyzing(false);
    }
  };

  const loadDraftIntoEditor = (draft: HRDraft) => {
    setSelectedTopicId(draft.topic);
    setFacts(draft.facts || {});
    setGeneratedAnswer(draft.generated_answer || '');
    setFinalAnswer(draft.final_answer || '');
    setCritiqueInput(draft.final_answer || '');
  };

  return (
    <div className="space-y-6 py-4">
      {/* Header */}
      <div className="space-y-1.5">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400">
          <MessageSquare className="w-3.5 h-3.5" />
          Specialized HR Interview Coach
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
          HR Answer Improvement Studio
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 max-w-2xl">
          Craft convincing, professional HR answers from your genuine facts without hallucination. Eliminate buzzwords, clichés, and vague claims.
        </p>
      </div>

      {/* Main Grid: Sidebar of Topics + Content Workspace */}
      <div className="grid lg:grid-cols-4 gap-6">
        {/* Left Topics List */}
        <div className="space-y-4">
          <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-2 shadow-sm">
            <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Interview Questions
            </h2>
            <div className="space-y-1">
              {topics.map((t) => {
                const isSelected = selectedTopicId === t.id;
                return (
                  <button
                    key={t.id}
                    onClick={() => {
                      setSelectedTopicId(t.id);
                      setGeneratedAnswer('');
                      setFinalAnswer('');
                      setFacts({});
                    }}
                    className={`w-full text-left px-3 py-2 rounded-xl text-xs font-medium transition-colors ${
                      isSelected
                        ? 'bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400 font-bold'
                        : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800'
                    }`}
                  >
                    {t.title}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Saved Drafts Box */}
          <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-3 shadow-sm">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Saved Drafts ({drafts.length})
            </h3>
            {drafts.length === 0 ? (
              <p className="text-[11px] text-slate-400">No drafts saved yet.</p>
            ) : (
              <div className="space-y-2">
                {drafts.map((d) => (
                  <div
                    key={d.id}
                    className="p-2.5 rounded-xl border border-slate-100 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-slate-50/50 dark:bg-slate-800/40 text-xs flex items-center justify-between gap-2"
                  >
                    <div
                      onClick={() => loadDraftIntoEditor(d)}
                      className="cursor-pointer truncate flex-1 font-medium text-slate-800 dark:text-slate-200"
                    >
                      {d.topic.replace(/_/g, ' ')}
                    </div>
                    <button
                      onClick={() => handleDeleteDraft(d.id)}
                      className="text-slate-400 hover:text-rose-500 p-1"
                      title="Delete draft"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Workspace (3 Columns) */}
        <div className="lg:col-span-3 space-y-6">
          {/* Framework Banner */}
          {currentTopic && (
            <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-bold text-slate-900 dark:text-white">
                  {currentTopic.title}
                </span>
                <span className="text-[11px] font-semibold text-brand-600 dark:text-brand-400">
                  Proven Framework
                </span>
              </div>
              <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 font-mono text-[11px] text-brand-700 dark:text-brand-300 border border-slate-200 dark:border-slate-800">
                {currentTopic.framework}
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                {currentTopic.description}
              </p>
            </div>
          )}

          {/* Tab Navigation */}
          <div className="flex border-b border-slate-200 dark:border-slate-800">
            <button
              onClick={() => setActiveTab('builder')}
              className={`px-4 py-2 text-xs font-bold border-b-2 transition-colors flex items-center gap-1.5 ${
                activeTab === 'builder'
                  ? 'border-brand-600 text-brand-600 dark:border-brand-400 dark:text-brand-400'
                  : 'border-transparent text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'
              }`}
            >
              <Wand2 className="w-3.5 h-3.5" />
              1. Personal Fact-to-Answer Builder
            </button>
            <button
              onClick={() => setActiveTab('critique')}
              className={`px-4 py-2 text-xs font-bold border-b-2 transition-colors flex items-center gap-1.5 ${
                activeTab === 'critique'
                  ? 'border-brand-600 text-brand-600 dark:border-brand-400 dark:text-brand-400'
                  : 'border-transparent text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'
              }`}
            >
              <Layers className="w-3.5 h-3.5" />
              2. Cliché Detector & Feedback
            </button>
          </div>

          {/* Tab 1: Fact Builder */}
          {activeTab === 'builder' && currentTopic && (
            <div className="space-y-6">
              <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
                <h3 className="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase">
                  Input Your Real Background Facts (No Hallucinations)
                </h3>

                <div className="space-y-3">
                  {currentTopic.prompt_fields.map((field) => (
                    <div key={field.key}>
                      <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                        {field.label}
                      </label>
                      <input
                        type="text"
                        value={facts[field.key] || ''}
                        onChange={(e) => handleFactChange(field.key, e.target.value)}
                        placeholder={field.placeholder}
                        className="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
                      />
                    </div>
                  ))}
                </div>

                <div className="pt-2">
                  <button
                    onClick={handleGenerate}
                    disabled={generating}
                    className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-semibold text-xs shadow-md shadow-brand-500/20 transition-all disabled:opacity-50"
                  >
                    {generating ? (
                      <>
                        <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        Generating Structured Answer...
                      </>
                    ) : (
                      <>
                        <Wand2 className="w-3.5 h-3.5" />
                        Generate Professional Answer
                      </>
                    )}
                  </button>
                </div>
              </div>

              {/* Editable Final Answer */}
              {finalAnswer && (
                <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-900 dark:text-white">
                      Your Polished Answer (Editable)
                    </span>
                    <button
                      onClick={handleSaveDraft}
                      disabled={saving}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 text-xs font-semibold hover:bg-slate-100 dark:hover:bg-slate-800"
                    >
                      <Save className="w-3.5 h-3.5 text-brand-500" />
                      {saving ? 'Saving...' : 'Save to Drafts'}
                    </button>
                  </div>

                  <textarea
                    value={finalAnswer}
                    onChange={(e) => setFinalAnswer(e.target.value)}
                    rows={6}
                    className="w-full p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs sm:text-sm text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500 leading-relaxed font-sans"
                  />

                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>Word Count: {finalAnswer.split(/\s+/).filter(Boolean).length} words</span>
                    <button
                      onClick={() => {
                        setCritiqueInput(finalAnswer);
                        setActiveTab('critique');
                      }}
                      className="font-semibold text-brand-600 hover:underline flex items-center gap-1"
                    >
                      Analyze this answer for clichés & metrics →
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Tab 2: Critique & Cliché Detector */}
          {activeTab === 'critique' && (
            <div className="space-y-6">
              <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
                <h3 className="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase">
                  Paste or Type Any HR Draft to Critique
                </h3>

                <textarea
                  value={critiqueInput}
                  onChange={(e) => setCritiqueInput(e.target.value)}
                  placeholder="Paste your answer draft here to check for buzzwords, vague language, and structure..."
                  rows={6}
                  className="w-full p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs sm:text-sm text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500 leading-relaxed font-sans"
                />

                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-400">
                    Words: {critiqueInput.split(/\s+/).filter(Boolean).length}
                  </span>
                  <button
                    onClick={handleAnalyzeDraft}
                    disabled={analyzing || !critiqueInput.trim()}
                    className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-semibold text-xs shadow-md shadow-brand-500/20 transition-all disabled:opacity-50"
                  >
                    {analyzing ? 'Analyzing...' : 'Run Cliché & Quality Audit'}
                  </button>
                </div>
              </div>

              {/* Analysis Results Display */}
              {analysis && (
                <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm text-xs">
                  <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
                    <span className="font-bold text-slate-900 dark:text-white">
                      Draft Quality Audit Result
                    </span>
                    <span className="font-bold px-3 py-1 rounded-full bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400 text-xs">
                      Impact Score: {analysis.score}/100
                    </span>
                  </div>

                  {/* Vague Clichés Warning */}
                  {analysis.vague_phrases.length > 0 && (
                    <div className="p-3.5 rounded-xl bg-rose-50/60 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900 space-y-1">
                      <div className="font-bold text-rose-700 dark:text-rose-400 flex items-center gap-1.5">
                        <AlertTriangle className="w-4 h-4" /> Detected Overused Clichés & Flaws
                      </div>
                      <ul className="list-disc list-inside text-rose-800 dark:text-rose-300 space-y-0.5">
                        {analysis.vague_phrases.map((v, i) => (
                          <li key={i}>{v}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Strengths */}
                  <div className="p-3.5 rounded-xl bg-emerald-50/60 dark:bg-emerald-950/20 border border-emerald-100 dark:border-emerald-900 space-y-1">
                    <div className="font-bold text-emerald-700 dark:text-emerald-400 flex items-center gap-1.5">
                      <CheckCircle className="w-4 h-4" /> Well-Executed Elements
                    </div>
                    <ul className="list-disc list-inside text-emerald-800 dark:text-emerald-300 space-y-0.5">
                      {analysis.strengths.map((s, i) => (
                        <li key={i}>{s}</li>
                      ))}
                    </ul>
                  </div>

                  {/* Coaching Tips */}
                  <div className="p-3.5 rounded-xl bg-indigo-50/60 dark:bg-indigo-950/20 border border-indigo-100 dark:border-indigo-900 space-y-1">
                    <div className="font-bold text-indigo-700 dark:text-indigo-400 flex items-center gap-1.5">
                      <Sparkles className="w-4 h-4" /> Actionable Coaching Tips
                    </div>
                    <ul className="list-disc list-inside text-indigo-800 dark:text-indigo-300 space-y-0.5">
                      {analysis.coaching_tips.map((t, i) => (
                        <li key={i}>{t}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
