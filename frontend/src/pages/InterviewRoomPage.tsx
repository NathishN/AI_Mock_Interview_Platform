import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  Mic,
  MicOff,
  Sparkles,
  Send,
  AlertCircle,
  Award,
  CheckCircle,
  Clock,
  ArrowRight,
  ShieldAlert,
  ChevronRight,
  HelpCircle,
  CornerDownRight,
} from 'lucide-react';
import { interviewsApi, InterviewSessionDetail, InterviewTurn } from '../api/interviews';

const PRESETS = [
  {
    id: 'hr_round',
    title: 'HR Round',
    time: '15 mins',
    desc: 'Self-intro, strengths, weaknesses, cultural fit & salary discussions.',
    stage: 'HR',
    mode: 'hr',
    numQuestions: 4,
    difficulty: 'Beginner',
  },
  {
    id: 'technical_interview',
    title: 'Technical Interview',
    time: '30 mins',
    desc: 'Data structures, OOP, SQL, algorithms, and system architecture fundamentals.',
    stage: 'Technical',
    mode: 'technical',
    numQuestions: 6,
    difficulty: 'Intermediate',
  },
  {
    id: 'final_interview',
    title: 'Final Round',
    time: '20 mins',
    desc: 'Mixed technical defense, situational STAR questions, and workplace adaptability.',
    stage: 'Final',
    mode: 'mixed',
    numQuestions: 5,
    difficulty: 'Intermediate',
  },
  {
    id: 'full_mock',
    title: 'Full Mock Interview',
    time: '45 mins',
    desc: 'Comprehensive end-to-end evaluation spanning coding, system design, and HR.',
    stage: 'Technical',
    mode: 'mixed',
    numQuestions: 8,
    difficulty: 'Intermediate',
  },
  {
    id: 'weakness_improvement',
    title: 'Weakness Improvement',
    time: '15 mins',
    desc: 'Targeted coaching probing your specific development areas with deep follow-ups.',
    stage: 'Technical',
    mode: 'mixed',
    numQuestions: 4,
    difficulty: 'Beginner',
  },
];

export const InterviewRoomPage: React.FC = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();

  // Setup state (for /interview/new)
  const [selectedPreset, setSelectedPreset] = useState('technical_interview');
  const [targetRole, setTargetRole] = useState('Software Development Engineer');
  const [company, setCompany] = useState('TCS');
  const [isCreating, setIsCreating] = useState(false);

  // Active interview state (for /interview/:sessionId)
  const [session, setSession] = useState<InterviewSessionDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [answerText, setAnswerText] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [speechError, setSpeechError] = useState<string | null>(null);

  const recognitionRef = useRef<any>(null);

  // Load session if sessionId is provided
  useEffect(() => {
    if (sessionId) {
      const loadSession = async () => {
        try {
          setLoading(true);
          const data = await interviewsApi.getSession(sessionId);
          setSession(data);
          if (data.status === 'completed') {
            navigate(`/interview/${sessionId}/results`, { replace: true });
          }
        } catch (err) {
          console.error(err);
        } finally {
          setLoading(false);
        }
      };
      loadSession();
    }
  }, [sessionId, navigate]);

  // Speech Recognition setup (Web Speech API)
  useEffect(() => {
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-IN'; // Indian English

      recognition.onresult = (event: any) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        setAnswerText((prev) => (prev ? `${prev} ${transcript}` : transcript));
      };

      recognition.onerror = (e: any) => {
        console.warn('Speech recognition error:', e.error);
        setIsListening(false);
        if (e.error === 'not-allowed') {
          setSpeechError('Microphone access was denied. Please allow microphone permissions in your browser.');
        }
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }
  }, []);

  const toggleListening = () => {
    if (!recognitionRef.current) {
      setSpeechError('Speech recognition is not supported in this browser. Please type your answer.');
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      setSpeechError(null);
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch (err) {
        console.error(err);
      }
    }
  };

  // Handle Starting a New Session
  const handleStartSession = async () => {
    try {
      setIsCreating(true);
      const preset = PRESETS.find((p) => p.id === selectedPreset)!;
      const newSession = await interviewsApi.createSession({
        target_role: targetRole,
        company: company === 'General' ? undefined : company,
        interview_stage: preset.stage,
        difficulty: preset.difficulty,
        duration_minutes: Number(preset.time.split(' ')[0]),
        num_questions: preset.numQuestions,
        mode: preset.mode,
        preset: preset.id,
      });
      navigate(`/interview/${newSession.id}`);
    } catch (err) {
      console.error(err);
    } finally {
      setIsCreating(false);
    }
  };

  // Handle Answer Submission
  const handleSubmitAnswer = async () => {
    if (!answerText.trim() || !session) return;

    if (isListening && recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
    }

    try {
      setSubmitting(true);
      const updated = await interviewsApi.submitAnswer(session.id, answerText.trim());
      setSession(updated);
      setAnswerText('');

      if (updated.status === 'completed') {
        navigate(`/interview/${session.id}/results`);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleFinishEarly = async () => {
    if (!session) return;
    try {
      await interviewsApi.finishEarly(session.id);
      navigate(`/interview/${session.id}/results`);
    } catch (err) {
      console.error(err);
    }
  };

  // View: Setup Screen when no sessionId
  if (!sessionId) {
    return (
      <div className="max-w-4xl mx-auto py-8 space-y-8">
        <div className="text-center space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400">
            <Sparkles className="w-3.5 h-3.5" />
            Adaptive AI Mock Interview Room
          </div>
          <h1 className="text-2xl sm:text-4xl font-extrabold text-slate-900 dark:text-white">
            Configure Your Mock Interview
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 max-w-xl mx-auto">
            Choose a suggested interview preset or target specific companies. The AI interviewer adapts question difficulty and challenges vague responses.
          </p>
        </div>

        {/* Preset Selection */}
        <div className="space-y-3">
          <label className="block text-xs font-bold text-slate-700 dark:text-slate-300">
            Suggested Presets
          </label>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {PRESETS.map((preset) => {
              const isSelected = selectedPreset === preset.id;
              return (
                <div
                  key={preset.id}
                  onClick={() => setSelectedPreset(preset.id)}
                  className={`p-4 rounded-2xl border cursor-pointer transition-all space-y-2 ${
                    isSelected
                      ? 'border-brand-500 bg-brand-50/50 dark:bg-brand-950/40 ring-2 ring-brand-500/20'
                      : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:border-slate-300 dark:hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-bold text-slate-900 dark:text-white">
                      {preset.title}
                    </span>
                    <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                      {preset.time}
                    </span>
                  </div>
                  <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                    {preset.desc}
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Custom Controls */}
        <div className="grid sm:grid-cols-2 gap-4 p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Target Role
            </label>
            <input
              type="text"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g. Software Development Engineer"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Company Context
            </label>
            <select
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500"
            >
              <option value="TCS">TCS (Tata Consultancy Services)</option>
              <option value="Infosys">Infosys</option>
              <option value="Amazon">Amazon</option>
              <option value="Google">Google</option>
              <option value="Accenture">Accenture</option>
              <option value="Wipro">Wipro</option>
              <option value="General">General Tech Company</option>
            </select>
          </div>
        </div>

        <div className="text-center pt-2">
          <button
            onClick={handleStartSession}
            disabled={isCreating}
            className="px-8 py-3.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-sm shadow-lg shadow-brand-500/25 transition-all inline-flex items-center gap-2 hover:scale-105 disabled:opacity-50"
          >
            {isCreating ? 'Setting Up Room...' : 'Launch Interview Session'}
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    );
  }

  // View: Active Interview Room
  if (loading || !session) {
    return (
      <div className="py-24 text-center text-xs text-slate-500">
        <div className="w-7 h-7 border-3 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
        Connecting to Interview Room...
      </div>
    );
  }

  // Find active turn waiting for answer
  const activeTurn = session.turns.find((t) => t.status === 'asked');
  const evaluatedTurns = session.turns.filter((t) => t.status === 'evaluated');
  const currentSequence = activeTurn ? activeTurn.sequence : session.turns.length;
  const targetCount = session.config?.num_questions || 5;

  return (
    <div className="max-w-4xl mx-auto py-6 space-y-6">
      {/* Session Progress Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></div>
          <div>
            <div className="text-xs font-bold text-slate-900 dark:text-white">
              {session.config?.target_role || 'SDE'} Round • {session.config?.company || 'General'}
            </div>
            <div className="text-[11px] text-slate-500 dark:text-slate-400">
              Question {currentSequence} of {targetCount} • Adaptive Difficulty: {session.adaptive_state?.current_difficulty || 'Intermediate'}
            </div>
          </div>
        </div>

        <button
          onClick={handleFinishEarly}
          className="text-xs font-semibold text-slate-500 hover:text-rose-600 dark:text-slate-400 dark:hover:text-rose-400 px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-800 transition-colors"
        >
          Finish Early & View Report
        </button>
      </div>

      {/* Active Question Box */}
      {activeTurn && (
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border-2 border-brand-500/30 dark:border-brand-500/20 shadow-md space-y-6">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400">
              Interviewer Question #{activeTurn.sequence}
              {activeTurn.is_follow_up && ' (Adaptive Follow-up)'}
            </span>
            <span className="text-[11px] font-medium text-slate-400">
              {activeTurn.topic || 'Interview Stage'}
            </span>
          </div>

          <h2 className="text-lg sm:text-xl font-bold text-slate-900 dark:text-white leading-relaxed">
            "{activeTurn.question_text}"
          </h2>

          {/* Answer Input */}
          <div className="space-y-3">
            <div className="relative">
              <textarea
                value={answerText}
                onChange={(e) => setAnswerText(e.target.value)}
                placeholder="Type your response here, or click the microphone to speak naturally..."
                rows={5}
                className="w-full p-4 rounded-2xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs sm:text-sm text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-brand-500 leading-relaxed font-sans"
              />
            </div>

            {speechError && (
              <p className="text-xs text-rose-500 flex items-center gap-1.5">
                <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                {speechError}
              </p>
            )}

            <div className="flex items-center justify-between gap-3 pt-1">
              <button
                type="button"
                onClick={toggleListening}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold border transition-all ${
                  isListening
                    ? 'bg-rose-50 border-rose-300 text-rose-600 dark:bg-rose-950/60 dark:border-rose-900 animate-pulse'
                    : 'border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
                }`}
              >
                {isListening ? <MicOff className="w-4 h-4 text-rose-500" /> : <Mic className="w-4 h-4" />}
                {isListening ? 'Listening (Click to stop)' : 'Voice Input (Speech-to-Text)'}
              </button>

              <button
                onClick={handleSubmitAnswer}
                disabled={submitting || !answerText.trim()}
                className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs shadow-md shadow-brand-500/20 transition-all disabled:opacity-50"
              >
                {submitting ? (
                  <>
                    <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    AI Evaluating Answer...
                  </>
                ) : (
                  <>
                    Submit Answer
                    <Send className="w-3.5 h-3.5" />
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Evaluated Turns History / Coaching Feedback */}
      {evaluatedTurns.length > 0 && (
        <div className="space-y-4 pt-4">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">
            Interview Transcripts & AI Marks ({evaluatedTurns.length})
          </h3>

          <div className="space-y-4">
            {evaluatedTurns.map((turn) => {
              const ev = turn.evaluation;
              return (
                <div
                  key={turn.id}
                  className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-4 text-xs shadow-sm"
                >
                  <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
                    <span className="font-bold text-slate-800 dark:text-slate-200">
                      Question #{turn.sequence}: {turn.question_text}
                    </span>
                    <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400">
                      Score: {turn.overall_score}/100
                    </span>
                  </div>

                  {/* Candidate Answer */}
                  <div className="space-y-1">
                    <span className="text-[11px] font-semibold text-slate-400 uppercase">
                      Your Answer:
                    </span>
                    <p className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 text-slate-700 dark:text-slate-300 italic">
                      "{turn.answer_text}"
                    </p>
                  </div>

                  {/* Feedback Breakdown */}
                  {ev && (
                    <div className="space-y-3 pt-2">
                      {/* Dimension Marks */}
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                        {ev.dimension_scores?.map((d: any, idx: number) => (
                          <div
                            key={idx}
                            className="p-2.5 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/30 space-y-0.5"
                          >
                            <div className="text-[10px] text-slate-400 truncate">{d.name}</div>
                            <div className="font-bold text-slate-900 dark:text-white">
                              {d.score}/10{' '}
                              <span className="text-[10px] font-normal text-slate-400">
                                ({d.weight}%)
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>

                      {/* Strengths & Missing Points */}
                      <div className="grid sm:grid-cols-2 gap-3 pt-1">
                        {ev.strengths?.length > 0 && (
                          <div className="p-3 rounded-xl bg-emerald-50/60 dark:bg-emerald-950/20 border border-emerald-100 dark:border-emerald-900/50 space-y-1">
                            <span className="font-bold text-emerald-700 dark:text-emerald-400 flex items-center gap-1">
                              <CheckCircle className="w-3.5 h-3.5" /> Strengths
                            </span>
                            <ul className="list-disc list-inside text-emerald-800 dark:text-emerald-300 space-y-0.5">
                              {ev.strengths.map((s: string, i: number) => (
                                <li key={i}>{s}</li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {ev.missing_points?.length > 0 && (
                          <div className="p-3 rounded-xl bg-amber-50/60 dark:bg-amber-950/20 border border-amber-100 dark:border-amber-900/50 space-y-1">
                            <span className="font-bold text-amber-700 dark:text-amber-400 flex items-center gap-1">
                              <AlertCircle className="w-3.5 h-3.5" /> Improvement Areas
                            </span>
                            <ul className="list-disc list-inside text-amber-800 dark:text-amber-300 space-y-0.5">
                              {ev.missing_points.map((m: string, i: number) => (
                                <li key={i}>{m}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>

                      {/* Model Revision */}
                      {ev.improved_answer && (
                        <div className="p-3 rounded-xl bg-brand-50/40 dark:bg-brand-950/20 border border-brand-100 dark:border-brand-900/40 space-y-1">
                          <span className="font-bold text-brand-700 dark:text-brand-400 flex items-center gap-1">
                            <Sparkles className="w-3.5 h-3.5" /> Suggested Revision
                          </span>
                          <p className="text-slate-700 dark:text-slate-300 whitespace-pre-wrap">
                            {ev.improved_answer}
                          </p>
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
    </div>
  );
};
