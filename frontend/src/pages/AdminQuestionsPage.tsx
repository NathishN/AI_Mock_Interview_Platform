import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  Search,
  Plus,
  Edit2,
  Trash2,
  CheckCircle,
  AlertCircle,
  X,
  BookOpen,
} from 'lucide-react';
import { questionsApi, Question } from '../api/questions';
import { adminApi } from '../api/admin';

export const AdminQuestionsPage: React.FC = () => {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [totalCount, setTotalCount] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [category, setCategory] = useState('All');
  const [loading, setLoading] = useState(true);

  // Edit / Create modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState<Partial<Question> | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      const params: Record<string, any> = { limit: 50 };
      if (category !== 'All') params.category = category;
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
  }, [category]);

  const handleOpenCreate = () => {
    setEditingQuestion({
      id: `custom-${Date.now()}`,
      category: 'HR',
      subcategory: 'Custom Topic',
      difficulty: 'Intermediate',
      question: '',
      reference_answer: 'Illustrative model answer with concrete steps.',
      key_points: ['Key concept 1', 'Key concept 2'],
      evaluation_criteria: ['Clarity', 'Relevance'],
      common_mistakes: ['Being too vague'],
      follow_up_questions: ['Can you provide a specific metric?'],
      target_roles: ['Software Development Engineer'],
      tags: ['custom', 'campus'],
      is_active: true,
    });
    setFormError(null);
    setModalOpen(true);
  };

  const handleOpenEdit = (q: Question) => {
    setEditingQuestion({ ...q });
    setFormError(null);
    setModalOpen(true);
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm(`Are you sure you want to delete question '${id}'?`)) return;
    try {
      await adminApi.deleteQuestion(id);
      setQuestions((prev) => prev.filter((q) => q.id !== id));
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to delete question');
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingQuestion?.question?.trim() || !editingQuestion?.reference_answer?.trim()) {
      setFormError('Question text and Reference answer are strictly required.');
      return;
    }

    try {
      setSaving(true);
      setFormError(null);

      // Check if updating existing or creating new
      const isExisting = questions.some((q) => q.id === editingQuestion.id);
      if (isExisting && editingQuestion.id) {
        await adminApi.updateQuestion(editingQuestion.id, editingQuestion);
      } else {
        await adminApi.createQuestion(editingQuestion);
      }

      setModalOpen(false);
      await fetchQuestions();
    } catch (err: any) {
      setFormError(err.response?.data?.detail || 'Error saving question to database');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6 py-4">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-50 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400">
            <ShieldCheck className="w-3.5 h-3.5" />
            Administrative Access
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
            Knowledge Base Question Manager
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Audit, edit, and add interview questions stored persistently in PostgreSQL.
          </p>
        </div>

        <button
          onClick={handleOpenCreate}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs shadow-md transition-all"
        >
          <Plus className="w-4 h-4" />
          Add New Question
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-4 shadow-sm text-xs">
        <div className="flex flex-1 items-center gap-2 max-w-md">
          <Search className="w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && fetchQuestions()}
            placeholder="Search questions or ID..."
            className="w-full px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
          />
        </div>

        <div className="flex items-center gap-3">
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
          >
            <option value="All">All Categories</option>
            <option value="HR">HR</option>
            <option value="Behavioral">Behavioral</option>
            <option value="Resume & Projects">Resume & Projects</option>
            <option value="Python">Python</option>
            <option value="SQL & Analytics">SQL & Analytics</option>
            <option value="ML, AI & GenAI">ML, AI & GenAI</option>
            <option value="Company & Workplace">Company & Workplace</option>
            <option value="Coding">Coding</option>
          </select>
          <span className="text-slate-400 font-medium">Total: {totalCount} records</span>
        </div>
      </div>

      {/* Table */}
      {loading ? (
        <div className="py-16 text-center text-xs text-slate-500">
          <div className="w-6 h-6 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
          Loading questions...
        </div>
      ) : (
        <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 overflow-hidden shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 dark:bg-slate-800/60 border-b border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 font-semibold">
                <tr>
                  <th className="py-3 px-4">ID</th>
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Difficulty</th>
                  <th className="py-3 px-4">Question</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {questions.map((q) => (
                  <tr key={q.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30">
                    <td className="py-3 px-4 font-mono font-bold text-slate-400">
                      {q.id}
                    </td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400">
                        {q.category}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded text-[10px] font-semibold text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-800">
                        {q.difficulty}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-medium text-slate-800 dark:text-slate-200 max-w-md truncate">
                      {q.question}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleOpenEdit(q)}
                          className="p-1 text-slate-400 hover:text-brand-600"
                          title="Edit question"
                        >
                          <Edit2 className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => handleDelete(q.id)}
                          className="p-1 text-slate-400 hover:text-rose-600"
                          title="Delete question"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Edit / Create Question Modal */}
      {modalOpen && editingQuestion && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="max-w-2xl w-full bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto text-xs">
            <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-slate-900 dark:text-white">
                {editingQuestion.id ? `Edit Question: ${editingQuestion.id}` : 'Create New Question'}
              </h3>
              <button
                onClick={() => setModalOpen(false)}
                className="text-slate-400 hover:text-slate-600"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {formError && (
              <div className="p-3 rounded-xl bg-rose-50 text-rose-600 border border-rose-200 text-xs flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{formError}</span>
              </div>
            )}

            <form onSubmit={handleSave} className="space-y-4">
              <div className="grid sm:grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold mb-1">Category</label>
                  <select
                    value={editingQuestion.category || 'HR'}
                    onChange={(e) =>
                      setEditingQuestion({ ...editingQuestion, category: e.target.value })
                    }
                    className="w-full px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white"
                  >
                    <option value="HR">HR</option>
                    <option value="Behavioral">Behavioral</option>
                    <option value="Resume & Projects">Resume & Projects</option>
                    <option value="Python">Python</option>
                    <option value="SQL & Analytics">SQL & Analytics</option>
                    <option value="ML, AI & GenAI">ML, AI & GenAI</option>
                    <option value="Company & Workplace">Company & Workplace</option>
                    <option value="Coding">Coding</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold mb-1">Difficulty</label>
                  <select
                    value={editingQuestion.difficulty || 'Intermediate'}
                    onChange={(e) =>
                      setEditingQuestion({
                        ...editingQuestion,
                        difficulty: e.target.value as any,
                      })
                    }
                    className="w-full px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white"
                  >
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block font-semibold mb-1">Question Prompt</label>
                <textarea
                  rows={2}
                  value={editingQuestion.question || ''}
                  onChange={(e) =>
                    setEditingQuestion({ ...editingQuestion, question: e.target.value })
                  }
                  className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
                />
              </div>

              <div>
                <label className="block font-semibold mb-1">Reference Answer / Model Response</label>
                <textarea
                  rows={5}
                  value={editingQuestion.reference_answer || ''}
                  onChange={(e) =>
                    setEditingQuestion({ ...editingQuestion, reference_answer: e.target.value })
                  }
                  className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2 border-t border-slate-100 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setModalOpen(false)}
                  className="px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={saving}
                  className="px-5 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold disabled:opacity-50"
                >
                  {saving ? 'Saving...' : 'Save Question'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
