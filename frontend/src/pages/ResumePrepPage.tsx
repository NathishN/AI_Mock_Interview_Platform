import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  UploadCloud,
  FileText,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  Play,
  ArrowRight,
  RefreshCw,
  ChevronDown,
  ChevronUp,
  Award,
  Mic,
  MicOff,
  Send,
  Trash2,
  ShieldCheck,
  Layers,
  Database,
  Cpu,
  Code2,
  HelpCircle,
  Clock,
  ExternalLink,
} from 'lucide-react';
import { resumesApi, ResumeDetail, ResumeSummary, ResumeQuestion } from '../api/resumes';

const POPULAR_ROLES = [
  'Software Development Engineer',
  'Full Stack Developer',
  'Frontend Engineer',
  'Backend Engineer',
  'Data Analyst / Scientist',
  'AI / ML Engineer',
  'DevOps / Cloud Engineer',
];

export const ResumePrepPage: React.FC = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Upload & Form State
  const [targetRole, setTargetRole] = useState('Software Development Engineer');
  const [activeUploadTab, setActiveUploadTab] = useState<'upload' | 'paste'>('upload');
  const [activeViewTab, setActiveViewTab] = useState<'questions' | 'analysis'>('questions');
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [pastedText, setPastedText] = useState('');

  // Loading & Progress State
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisStep, setAnalysisStep] = useState(0);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Resume Data State
  const [currentResume, setCurrentResume] = useState<ResumeDetail | null>(null);
  const [resumeHistory, setResumeHistory] = useState<ResumeSummary[]>([]);
  const [loadingInitial, setLoadingInitial] = useState(true);
  const [startingInterview, setStartingInterview] = useState(false);
  const [expandedQuestionId, setExpandedQuestionId] = useState<string | null>(null);

  // In-place Quick Practice State for Questions
  const [practiceQuestionId, setPracticeQuestionId] = useState<string | null>(null);
  const [practiceAnswer, setPracticeAnswer] = useState<string>('');
  const [evaluatingPractice, setEvaluatingPractice] = useState(false);
  const [practiceResult, setPracticeResult] = useState<{ [qId: string]: any }>({});
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<any>(null);

  const analysisSteps = [
    'Extracting document content & structure...',
    'Identifying technical skills, frameworks & databases...',
    'Auditing claimed projects and technical metrics...',
    'Synthesizing tailored interview defense questions...',
  ];

  // Fetch initial latest resume and history
  useEffect(() => {
    const fetchExisting = async () => {
      try {
        setLoadingInitial(true);
        const [latestRes, historyRes] = await Promise.allSettled([
          resumesApi.getLatest(),
          resumesApi.list(),
        ]);

        if (latestRes.status === 'fulfilled' && latestRes.value) {
          setCurrentResume(latestRes.value);
          if (latestRes.value.target_role) {
            setTargetRole(latestRes.value.target_role);
          }
        }
        if (historyRes.status === 'fulfilled') {
          setResumeHistory(historyRes.value || []);
        }
      } catch (err) {
        console.warn('No active resume found yet', err);
      } finally {
        setLoadingInitial(false);
      }
    };

    fetchExisting();
  }, []);

  // Analysis progress animation
  useEffect(() => {
    let timer: any;
    if (analyzing) {
      setAnalysisStep(0);
      timer = setInterval(() => {
        setAnalysisStep((prev) => (prev < analysisSteps.length - 1 ? prev + 1 : prev));
      }, 2200);
    }
    return () => clearInterval(timer);
  }, [analyzing]);

  // Speech recognition setup for in-place practice
  useEffect(() => {
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-IN';

      recognition.onresult = (event: any) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        setPracticeAnswer((prev) => (prev ? `${prev} ${transcript}` : transcript));
      };

      recognition.onerror = () => {
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }
  }, []);

  const toggleListening = () => {
    if (!recognitionRef.current) return;
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch (err) {
        console.error(err);
      }
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelected(e.target.files[0]);
    }
  };

  const handleFileSelected = (file: File) => {
    const validTypes = ['.pdf', '.docx', '.txt'];
    const hasValidExt = validTypes.some((ext) => file.name.toLowerCase().endsWith(ext));
    if (!hasValidExt) {
      setErrorMsg('Please upload a PDF, DOCX, or TXT file.');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setErrorMsg('File exceeds 10MB limit.');
      return;
    }
    setErrorMsg(null);
    setSelectedFile(file);
  };

  const handleAnalyzeUpload = async () => {
    if (!selectedFile) {
      setErrorMsg('Please select a resume file to upload.');
      return;
    }

    try {
      setAnalyzing(true);
      setErrorMsg(null);
      const data = await resumesApi.uploadFile(selectedFile, targetRole);
      setCurrentResume(data);
      const updatedList = await resumesApi.list();
      setResumeHistory(updatedList);
      setSelectedFile(null);
      setActiveViewTab('questions');
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Failed to analyze resume. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleAnalyzePasted = async () => {
    if (!pastedText.trim() || pastedText.trim().length < 50) {
      setErrorMsg('Please paste at least 50 characters of resume text.');
      return;
    }

    try {
      setAnalyzing(true);
      setErrorMsg(null);
      const data = await resumesApi.uploadText(pastedText, targetRole);
      setCurrentResume(data);
      const updatedList = await resumesApi.list();
      setResumeHistory(updatedList);
      setPastedText('');
      setActiveViewTab('questions');
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Failed to analyze resume text. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleStartInterview = async () => {
    if (!currentResume) return;
    try {
      setStartingInterview(true);
      const session = await resumesApi.startInterview(currentResume.id, {
        target_role: targetRole,
        company: 'Target Tech Placement',
        num_questions: currentResume.analysis.generated_questions?.length || 5,
      });
      navigate(`/interview/${session.id}`);
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Could not start mock interview session.');
      setStartingInterview(false);
    }
  };

  const handleSelectHistoryResume = async (resumeId: string) => {
    try {
      setLoadingInitial(true);
      const data = await resumesApi.getById(resumeId);
      setCurrentResume(data);
      if (data.target_role) setTargetRole(data.target_role);
      setActiveViewTab('questions');
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingInitial(false);
    }
  };

  const handleDeleteResume = async (resumeId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await resumesApi.delete(resumeId);
      const updated = resumeHistory.filter((r) => r.id !== resumeId);
      setResumeHistory(updated);
      if (currentResume?.id === resumeId) {
        if (updated.length > 0) {
          handleSelectHistoryResume(updated[0].id);
        } else {
          setCurrentResume(null);
        }
      }
    } catch (err) {
      console.error('Failed to delete resume', err);
    }
  };

  const handleEvaluatePracticeQuestion = async (q: ResumeQuestion) => {
    if (!practiceAnswer.trim() || !currentResume) return;
    try {
      setEvaluatingPractice(true);
      const evalData = await resumesApi.evaluateQuestion(currentResume.id, {
        question_id: q.id,
        question_text: q.question,
        answer_text: practiceAnswer.trim(),
        target_role: targetRole,
        rubric_key: q.rubric_key || 'technical',
      });
      setPracticeResult((prev) => ({
        ...prev,
        [q.id]: evalData,
      }));
    } catch (err: any) {
      console.error(err);
    } finally {
      setEvaluatingPractice(false);
    }
  };

  const getScoreBadge = (score: number) => {
    if (score >= 80) {
      return {
        bg: 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800',
        label: 'Placement Ready',
      };
    }
    if (score >= 70) {
      return {
        bg: 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/40 dark:text-blue-300 dark:border-blue-800',
        label: 'Competitive',
      };
    }
    if (score >= 60) {
      return {
        bg: 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800',
        label: 'Needs Polish',
      };
    }
    return {
      bg: 'bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-950/40 dark:text-rose-300 dark:border-rose-800',
      label: 'Action Required',
    };
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-16">
      {/* Clean Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 text-xs font-semibold border border-blue-200 dark:border-blue-800">
            <Sparkles className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
            Resume Defense & Analysis
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            Resume Analysis & Interview Defense
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400 max-w-2xl">
            Upload your resume to extract your tech stack, audit ATS placement readiness, and prepare for the exact questions recruiters will ask.
          </p>
        </div>

        {/* Quick Launch CTA if resume exists */}
        {currentResume && (
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={handleStartInterview}
              disabled={startingInterview}
              className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl font-bold text-sm bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white shadow-sm transition-all focus:outline-none focus:ring-2 focus:ring-blue-500/40 cursor-pointer disabled:opacity-50"
            >
              {startingInterview ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin text-white" />
                  <span>Entering Mock Room...</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 fill-current text-white" />
                  <span>Launch Resume Mock Interview</span>
                  <ArrowRight className="w-4 h-4 text-white" />
                </>
              )}
            </button>
          </div>
        )}
      </div>

      {/* Upload & Setup Section */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 dark:border-slate-800 pb-4">
          <div>
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <UploadCloud className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              Upload or Update Resume
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              PDF, DOCX, or TXT (Max 10MB). Text is parsed securely and used to generate custom interview questions.
            </p>
          </div>

          {/* Mode Switcher */}
          <div className="inline-flex p-1 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
            <button
              type="button"
              onClick={() => setActiveUploadTab('upload')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                activeUploadTab === 'upload'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              Upload Document
            </button>
            <button
              type="button"
              onClick={() => setActiveUploadTab('paste')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                activeUploadTab === 'paste'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              Paste Text
            </button>
          </div>
        </div>

        {/* Target Job Role Selector */}
        <div className="space-y-2">
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 dark:text-slate-400">
            Target Placement Role
          </label>
          <div className="flex flex-wrap gap-2">
            {POPULAR_ROLES.map((role) => {
              const isSelected = targetRole === role;
              return (
                <button
                  key={role}
                  type="button"
                  onClick={() => setTargetRole(role)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-blue-600 text-white border-blue-600 shadow-xs font-semibold'
                      : 'bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/60'
                  }`}
                >
                  {role}
                </button>
              );
            })}
          </div>
        </div>

        {/* Error Notification */}
        {errorMsg && (
          <div className="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300 text-xs flex items-start gap-2.5">
            <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-rose-600 dark:text-rose-400" />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* Tab 1: File Dropzone */}
        {activeUploadTab === 'upload' && (
          <div className="space-y-4">
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all ${
                dragActive
                  ? 'border-blue-500 bg-blue-50/50 dark:bg-blue-950/30'
                  : 'border-slate-300 dark:border-slate-700 hover:border-blue-400 dark:hover:border-blue-500 bg-slate-50/60 dark:bg-slate-800/40'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={handleFileChange}
                className="hidden"
              />

              {selectedFile ? (
                <div className="flex flex-col items-center gap-2">
                  <div className="w-12 h-12 rounded-xl bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 flex items-center justify-center">
                    <FileText className="w-6 h-6" />
                  </div>
                  <span className="text-sm font-bold text-slate-900 dark:text-white">
                    {selectedFile.name}
                  </span>
                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    {(selectedFile.size / 1024).toFixed(1)} KB • Ready to analyze. Click or drag another file to replace.
                  </span>
                </div>
              ) : (
                <div className="flex flex-col items-center gap-2.5">
                  <div className="w-12 h-12 rounded-xl bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 flex items-center justify-center">
                    <UploadCloud className="w-6 h-6" />
                  </div>
                  <div>
                    <span className="text-sm font-bold text-slate-900 dark:text-white block">
                      Click to choose or drag and drop your resume file
                    </span>
                    <span className="text-xs text-slate-500 dark:text-slate-400 block mt-1">
                      PDF, DOCX, or plain TXT (Max 10MB)
                    </span>
                  </div>
                </div>
              )}
            </div>

            <div className="flex items-center justify-end">
              <button
                type="button"
                disabled={!selectedFile || analyzing}
                onClick={handleAnalyzeUpload}
                className="w-full sm:w-auto px-6 py-2.5 rounded-xl font-bold text-sm bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white shadow-sm transition-all focus:outline-none focus:ring-2 focus:ring-blue-500/40 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {analyzing ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin text-white" />
                    <span>Analyzing Resume with AI...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 text-white" />
                    <span>Analyze Resume & Generate Questions</span>
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* Tab 2: Paste Raw Text */}
        {activeUploadTab === 'paste' && (
          <div className="space-y-4">
            <textarea
              rows={6}
              value={pastedText}
              onChange={(e) => setPastedText(e.target.value)}
              placeholder="Paste your resume content here including project descriptions, tech stack, and experience..."
              className="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 p-4 text-xs sm:text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono"
            />

            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-500">
                {pastedText.length} characters (minimum 50 required)
              </span>
              <button
                type="button"
                disabled={pastedText.trim().length < 50 || analyzing}
                onClick={handleAnalyzePasted}
                className="px-6 py-2.5 rounded-xl font-bold text-sm bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white shadow-sm transition-all focus:outline-none focus:ring-2 focus:ring-blue-500/40 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {analyzing ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin text-white" />
                    <span>Analyzing Resume with AI...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 text-white" />
                    <span>Analyze Content & Generate Questions</span>
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* Step Progression Animation */}
        {analyzing && (
          <div className="p-4 rounded-xl bg-blue-50/70 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-900/60 space-y-2">
            <div className="flex items-center gap-2 text-xs font-semibold text-blue-700 dark:text-blue-300">
              <RefreshCw className="w-3.5 h-3.5 animate-spin" />
              <span>
                Step {analysisStep + 1} of 4: {analysisSteps[analysisStep]}
              </span>
            </div>
            <div className="w-full h-1.5 rounded-full bg-blue-200 dark:bg-blue-900 overflow-hidden">
              <div
                className="h-full bg-blue-600 transition-all duration-500 rounded-full"
                style={{ width: `${((analysisStep + 1) / 4) * 100}%` }}
              />
            </div>
          </div>
        )}

        {/* Previously Uploaded Resumes Quick Selector */}
        {resumeHistory.length > 0 && (
          <div className="pt-3 border-t border-slate-100 dark:border-slate-800">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 block mb-2">
              Uploaded Resumes ({resumeHistory.length})
            </span>
            <div className="flex flex-wrap gap-2">
              {resumeHistory.map((item) => {
                const isSelected = currentResume?.id === item.id;
                return (
                  <div
                    key={item.id}
                    onClick={() => handleSelectHistoryResume(item.id)}
                    className={`group px-3 py-1.5 rounded-xl border text-xs font-medium cursor-pointer transition-all flex items-center gap-2 ${
                      isSelected
                        ? 'bg-blue-50 dark:bg-blue-950/60 border-blue-500 text-blue-700 dark:text-blue-300 shadow-xs'
                        : 'bg-slate-50 dark:bg-slate-800/60 border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:border-slate-400'
                    }`}
                  >
                    <FileText className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400 shrink-0" />
                    <span className="font-semibold max-w-[140px] truncate">{item.filename}</span>
                    {item.ats_score !== undefined && item.ats_score !== null && (
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 font-bold">
                        ATS {item.ats_score}
                      </span>
                    )}
                    <button
                      type="button"
                      title="Delete resume"
                      onClick={(e) => handleDeleteResume(item.id, e)}
                      className="text-slate-400 hover:text-rose-600 dark:hover:text-rose-400 p-0.5 rounded transition-colors"
                    >
                      <Trash2 className="w-3 h-3" />
                    </button>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Active Resume Studio View */}
      {currentResume && (
        <div className="space-y-6">
          {/* Active Resume Bar & Tab Controls */}
          <div className="p-4 sm:p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold">
                <FileText className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-bold text-slate-900 dark:text-white truncate">
                    {currentResume.filename}
                  </h3>
                  {currentResume.analysis?.ats_score !== undefined && (
                    <span
                      className={`text-[11px] font-bold px-2 py-0.5 rounded-full border ${
                        getScoreBadge(currentResume.analysis.ats_score).bg
                      }`}
                    >
                      ATS {currentResume.analysis.ats_score}/100 •{' '}
                      {getScoreBadge(currentResume.analysis.ats_score).label}
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Target Role: <span className="font-semibold">{currentResume.target_role || targetRole}</span> •{' '}
                  {currentResume.analysis.generated_questions?.length || 0} tailored questions prepared
                </p>
              </div>
            </div>

            {/* View Switcher Tabs */}
            <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shrink-0">
              <button
                type="button"
                onClick={() => setActiveViewTab('questions')}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer flex items-center gap-1.5 ${
                  activeViewTab === 'questions'
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                <Sparkles className="w-3.5 h-3.5" />
                Tailored Questions ({currentResume.analysis.generated_questions?.length || 0})
              </button>
              <button
                type="button"
                onClick={() => setActiveViewTab('analysis')}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer flex items-center gap-1.5 ${
                  activeViewTab === 'analysis'
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                <Award className="w-3.5 h-3.5" />
                ATS & Vulnerabilities
              </button>
            </div>
          </div>

          {/* TAB 1: TAILORED INTERVIEW QUESTIONS */}
          {activeViewTab === 'questions' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                    Interview Questions Tailored to Your Projects & Stack
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    Test your defense answer for each question directly, or launch the mock interview room.
                  </p>
                </div>

                <button
                  type="button"
                  onClick={handleStartInterview}
                  disabled={startingInterview}
                  className="hidden sm:inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold bg-blue-600 hover:bg-blue-700 text-white shadow-xs transition-colors cursor-pointer"
                >
                  <Play className="w-3.5 h-3.5 fill-current" />
                  Start Full Mock Interview
                </button>
              </div>

              {/* Questions List */}
              <div className="space-y-3">
                {currentResume.analysis.generated_questions?.map((q, idx) => {
                  const isExpanded = expandedQuestionId === q.id;
                  const isPracticing = practiceQuestionId === q.id;
                  const questionResult = practiceResult[q.id];

                  return (
                    <div
                      key={q.id || idx}
                      className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm overflow-hidden transition-all"
                    >
                      {/* Question Header */}
                      <div className="p-4 sm:p-5 flex items-start justify-between gap-4">
                        <div className="space-y-2 flex-1">
                          <div className="flex flex-wrap items-center gap-2">
                            <span className="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800">
                              Question {idx + 1} • {q.category}
                            </span>
                            <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                              {q.topic}
                            </span>
                            <span className="text-[11px] font-medium text-slate-400">
                              Difficulty: {q.difficulty}
                            </span>
                          </div>

                          <h4 className="text-sm sm:text-base font-bold text-slate-900 dark:text-white leading-snug">
                            {q.question}
                          </h4>
                        </div>

                        {/* Actions */}
                        <div className="flex items-center gap-2 shrink-0 pt-1">
                          <button
                            type="button"
                            onClick={() => {
                              if (isPracticing) {
                                setPracticeQuestionId(null);
                              } else {
                                setPracticeQuestionId(q.id);
                                setPracticeAnswer('');
                                setExpandedQuestionId(q.id);
                              }
                            }}
                            className={`px-3 py-1.5 rounded-lg text-xs font-bold border transition-all cursor-pointer ${
                              isPracticing
                                ? 'bg-blue-600 text-white border-blue-600 shadow-xs'
                                : 'bg-white dark:bg-slate-800 text-blue-600 dark:text-blue-400 border-blue-200 dark:border-blue-800 hover:bg-blue-50 dark:hover:bg-blue-950/40'
                            }`}
                          >
                            {isPracticing ? 'Close Practice' : 'Practice Answer'}
                          </button>

                          <button
                            type="button"
                            onClick={() => setExpandedQuestionId(isExpanded ? null : q.id)}
                            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
                            aria-label="Toggle details"
                          >
                            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                          </button>
                        </div>
                      </div>

                      {/* Expandable Rationale & Checklist */}
                      {isExpanded && (
                        <div className="p-5 border-t border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/40 space-y-4 text-xs">
                          {q.interviewer_context && (
                            <div className="p-3.5 rounded-xl bg-blue-50/70 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-900/50 text-blue-800 dark:text-blue-200 space-y-1">
                              <span className="font-bold text-[11px] uppercase tracking-wider block text-blue-700 dark:text-blue-300">
                                Why Interviewers Probe This on Your Resume:
                              </span>
                              <p className="leading-relaxed">{q.interviewer_context}</p>
                            </div>
                          )}

                          {q.key_points && q.key_points.length > 0 && (
                            <div className="space-y-1.5">
                              <span className="font-bold text-slate-800 dark:text-slate-200 uppercase text-[11px] tracking-wider block">
                                Essential Points to Hit in Your Answer:
                              </span>
                              <ul className="space-y-1.5">
                                {q.key_points.map((pt, i) => (
                                  <li key={i} className="flex items-start gap-2 text-slate-700 dark:text-slate-300">
                                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400 mt-0.5 shrink-0" />
                                    <span>{pt}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {q.ideal_answer_outline && (
                            <div className="p-3.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-1">
                              <span className="font-bold text-[11px] uppercase tracking-wider text-slate-800 dark:text-slate-200 block">
                                Recommended Answer Framework:
                              </span>
                              <p className="text-slate-600 dark:text-slate-300 leading-relaxed font-sans">
                                {q.ideal_answer_outline}
                              </p>
                            </div>
                          )}

                          {/* IN-PLACE INTERACTIVE PRACTICE BOX */}
                          {isPracticing && (
                            <div className="p-4 rounded-xl bg-white dark:bg-slate-800/80 border-2 border-blue-500/30 dark:border-blue-500/20 shadow-sm space-y-3">
                              <div className="flex items-center justify-between">
                                <span className="font-bold text-slate-900 dark:text-white text-xs flex items-center gap-1.5">
                                  <Mic className="w-3.5 h-3.5 text-blue-600" />
                                  Your Response to Question #{idx + 1}
                                </span>
                                <span className="text-[11px] text-slate-400">
                                  Speak or type your defense answer
                                </span>
                              </div>

                              <textarea
                                rows={4}
                                value={practiceAnswer}
                                onChange={(e) => setPracticeAnswer(e.target.value)}
                                placeholder="Explain your project architecture, tech stack decisions, or technical challenge..."
                                className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-blue-500 font-sans"
                              />

                              <div className="flex items-center justify-between gap-2 pt-1">
                                <button
                                  type="button"
                                  onClick={toggleListening}
                                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all flex items-center gap-1.5 cursor-pointer ${
                                    isListening
                                      ? 'bg-rose-50 border-rose-300 text-rose-600 dark:bg-rose-950/60 dark:border-rose-900 animate-pulse'
                                      : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-slate-200'
                                  }`}
                                >
                                  {isListening ? <MicOff className="w-3.5 h-3.5 text-rose-600" /> : <Mic className="w-3.5 h-3.5" />}
                                  {isListening ? 'Listening...' : 'Voice Dictate'}
                                </button>

                                <button
                                  type="button"
                                  disabled={evaluatingPractice || !practiceAnswer.trim()}
                                  onClick={() => handleEvaluatePracticeQuestion(q)}
                                  className="px-4 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white font-bold text-xs shadow-xs transition-all disabled:opacity-50 cursor-pointer flex items-center gap-1.5"
                                >
                                  {evaluatingPractice ? (
                                    <>
                                      <RefreshCw className="w-3.5 h-3.5 animate-spin text-white" />
                                      <span>Grading Answer...</span>
                                    </>
                                  ) : (
                                    <>
                                      <Send className="w-3.5 h-3.5 text-white" />
                                      <span>Grade My Defense</span>
                                    </>
                                  )}
                                </button>
                              </div>

                              {/* In-place Grading Output */}
                              {questionResult && (
                                <div className="mt-4 p-4 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-3">
                                  <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-2">
                                    <span className="font-bold text-slate-900 dark:text-white">
                                      Defense Mark & Rubric Assessment:
                                    </span>
                                    <span className="text-xs font-extrabold px-2.5 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300">
                                      {questionResult.overall_score}/100 ({questionResult.performance_band})
                                    </span>
                                  </div>

                                  {questionResult.strengths && questionResult.strengths.length > 0 && (
                                    <div className="space-y-1">
                                      <span className="font-bold text-emerald-600 dark:text-emerald-400 block text-[11px] uppercase">
                                        What You Did Well:
                                      </span>
                                      <ul className="space-y-1 text-slate-700 dark:text-slate-300">
                                        {questionResult.strengths.map((s: string, idx: number) => (
                                          <li key={idx} className="flex items-start gap-1.5">
                                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 mt-0.5 shrink-0" />
                                            <span>{s}</span>
                                          </li>
                                        ))}
                                      </ul>
                                    </div>
                                  )}

                                  {questionResult.missing_points && questionResult.missing_points.length > 0 && (
                                    <div className="space-y-1">
                                      <span className="font-bold text-amber-600 dark:text-amber-400 block text-[11px] uppercase">
                                        Points You Missed:
                                      </span>
                                      <ul className="space-y-1 text-slate-700 dark:text-slate-300">
                                        {questionResult.missing_points.map((m: string, idx: number) => (
                                          <li key={idx} className="flex items-start gap-1.5">
                                            <AlertTriangle className="w-3.5 h-3.5 text-amber-500 mt-0.5 shrink-0" />
                                            <span>{m}</span>
                                          </li>
                                        ))}
                                      </ul>
                                    </div>
                                  )}

                                  {questionResult.follow_up_question && (
                                    <div className="p-3 rounded-lg bg-amber-50/70 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800 text-amber-900 dark:text-amber-200">
                                      <span className="font-bold block text-[11px] uppercase">
                                        Likely Follow-up From Interviewer:
                                      </span>
                                      <p className="italic mt-0.5">"{questionResult.follow_up_question}"</p>
                                    </div>
                                  )}
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* TAB 2: ATS SCORE, EXTRACTED SKILLS & VULNERABILITIES */}
          {activeViewTab === 'analysis' && (
            <div className="space-y-6">
              {/* Top Row: Score + Extracted Skills */}
              <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
                {/* ATS Score Card */}
                <div className="md:col-span-5 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
                      <Award className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                      ATS Placement Readiness
                    </h3>
                    <span
                      className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${
                        getScoreBadge(currentResume.analysis.ats_score).bg
                      }`}
                    >
                      {getScoreBadge(currentResume.analysis.ats_score).label}
                    </span>
                  </div>

                  {/* Circular Score Gauge */}
                  <div className="flex flex-col items-center justify-center py-4">
                    <div className="text-5xl font-black text-slate-900 dark:text-white tracking-tight">
                      {currentResume.analysis.ats_score}
                      <span className="text-xl font-medium text-slate-400">/100</span>
                    </div>
                    <span className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                      Algorithmic ATS & Interview Readiness Benchmark
                    </span>
                  </div>

                  {/* Sub-breakdown */}
                  {currentResume.analysis.ats_breakdown && (
                    <div className="space-y-2 pt-2 border-t border-slate-100 dark:border-slate-800 text-xs">
                      {Object.entries(currentResume.analysis.ats_breakdown).map(([k, v]) => {
                        const label = k.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
                        const val = typeof v === 'number' ? v : 70;
                        return (
                          <div key={k} className="space-y-1">
                            <div className="flex justify-between text-slate-600 dark:text-slate-400">
                              <span>{label}</span>
                              <span className="font-bold text-slate-900 dark:text-white">{val}%</span>
                            </div>
                            <div className="w-full h-1.5 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
                              <div
                                className="h-full bg-blue-600 rounded-full"
                                style={{ width: `${val}%` }}
                              />
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>

                {/* Extracted Skills Card */}
                <div className="md:col-span-7 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-4">
                  <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <Cpu className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                    Verified Skills & Technologies Extracted
                  </h3>

                  <div className="space-y-3 text-xs">
                    {/* Programming Languages */}
                    {currentResume.parsed_data?.skills?.languages && currentResume.parsed_data.skills.languages.length > 0 && (
                      <div className="space-y-1.5">
                        <span className="font-bold text-slate-600 dark:text-slate-400 block uppercase tracking-wider text-[10px]">
                          Programming Languages
                        </span>
                        <div className="flex flex-wrap gap-1.5">
                          {currentResume.parsed_data.skills.languages.map((lang, idx) => (
                            <span
                              key={idx}
                              className="px-2.5 py-1 rounded-md text-xs font-semibold bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800"
                            >
                              {lang}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Frameworks & Libraries */}
                    {currentResume.parsed_data?.skills?.frameworks_and_libraries && currentResume.parsed_data.skills.frameworks_and_libraries.length > 0 && (
                      <div className="space-y-1.5">
                        <span className="font-bold text-slate-600 dark:text-slate-400 block uppercase tracking-wider text-[10px]">
                          Frameworks & Libraries
                        </span>
                        <div className="flex flex-wrap gap-1.5">
                          {currentResume.parsed_data.skills.frameworks_and_libraries.map((f, idx) => (
                            <span
                              key={idx}
                              className="px-2.5 py-1 rounded-md text-xs font-semibold bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800"
                            >
                              {f}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Databases */}
                    {currentResume.parsed_data?.skills?.databases && currentResume.parsed_data.skills.databases.length > 0 && (
                      <div className="space-y-1.5">
                        <span className="font-bold text-slate-600 dark:text-slate-400 block uppercase tracking-wider text-[10px]">
                          Databases & Storage
                        </span>
                        <div className="flex flex-wrap gap-1.5">
                          {currentResume.parsed_data.skills.databases.map((d, idx) => (
                            <span
                              key={idx}
                              className="px-2.5 py-1 rounded-md text-xs font-semibold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800"
                            >
                              {d}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Tools */}
                    {currentResume.parsed_data?.skills?.tools_and_platforms && currentResume.parsed_data.skills.tools_and_platforms.length > 0 && (
                      <div className="space-y-1.5">
                        <span className="font-bold text-slate-600 dark:text-slate-400 block uppercase tracking-wider text-[10px]">
                          Platforms & Tools
                        </span>
                        <div className="flex flex-wrap gap-1.5">
                          {currentResume.parsed_data.skills.tools_and_platforms.map((t, idx) => (
                            <span
                              key={idx}
                              className="px-2.5 py-1 rounded-md text-xs font-semibold bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700"
                            >
                              {t}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Extracted Projects */}
              {currentResume.parsed_data?.projects && currentResume.parsed_data.projects.length > 0 && (
                <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-4">
                  <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <Code2 className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                    Key Resume Projects Identified ({currentResume.parsed_data.projects.length})
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {currentResume.parsed_data.projects.map((proj, idx) => (
                      <div
                        key={idx}
                        className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-800 space-y-2 text-xs"
                      >
                        <p className="font-bold text-slate-900 dark:text-white text-sm">{proj.title}</p>
                        <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                          {proj.summary}
                        </p>
                        {proj.technologies && proj.technologies.length > 0 && (
                          <div className="flex flex-wrap gap-1 pt-1">
                            {proj.technologies.map((t, i) => (
                              <span
                                key={i}
                                className="text-[10px] px-2 py-0.5 rounded font-semibold bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200"
                              >
                                {t}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Vulnerabilities & Strengths Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Flagged Risks */}
                <div className="bg-white dark:bg-slate-900 rounded-2xl border border-amber-200 dark:border-amber-900/50 p-6 shadow-sm space-y-3">
                  <h3 className="text-sm font-bold text-amber-700 dark:text-amber-400 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4" />
                    Interview Vulnerabilities & Grilling Areas
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    Interviewers quickly notice vague metrics or listed tools without clear project applications.
                  </p>
                  <ul className="space-y-2 pt-1 text-xs">
                    {currentResume.analysis.flagged_risks?.map((risk, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-slate-700 dark:text-slate-300">
                        <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5 shrink-0" />
                        <span>{risk}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Strengths */}
                <div className="bg-white dark:bg-slate-900 rounded-2xl border border-emerald-200 dark:border-emerald-900/50 p-6 shadow-sm space-y-3">
                  <h3 className="text-sm font-bold text-emerald-700 dark:text-emerald-400 flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4" />
                    Verified Strengths to Emphasize
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    Bring up these aspects in your self-introduction and project deep dives.
                  </p>
                  <ul className="space-y-2 pt-1 text-xs">
                    {currentResume.analysis.strengths?.map((str, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-slate-700 dark:text-slate-300">
                        <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400 mt-0.5 shrink-0" />
                        <span>{str}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
