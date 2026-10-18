import { apiClient } from './client';

export interface DimensionScore {
  name: string;
  score: number;
  weight: number;
  justification: string;
}

export interface EvaluationResult {
  overall_score: number;
  performance_band: string;
  dimension_scores: DimensionScore[];
  strengths: string[];
  missing_points: string[];
  mistakes: string[];
  clarity_feedback: string;
  ideal_answer: string;
  improved_answer: string;
  follow_up_question?: string | null;
  practice_recommendations: string[];
}

export interface InterviewTurn {
  id: string;
  session_id: string;
  sequence: number;
  question_id?: string | null;
  parent_turn_id?: string | null;
  question_text: string;
  is_follow_up: boolean;
  rubric_key?: string | null;
  difficulty?: string | null;
  topic?: string | null;
  answer_text?: string | null;
  answered_at?: string | null;
  status: 'asked' | 'evaluated' | 'evaluation_failed';
  evaluation?: EvaluationResult | null;
  overall_score?: number | null;
  eval_latency_ms?: number | null;
  eval_error?: string | null;
}

export interface InterviewSessionSummary {
  id: string;
  status: 'in_progress' | 'completed' | 'abandoned';
  config: Record<string, any>;
  started_at?: string | null;
  ended_at?: string | null;
  final_score?: number | null;
  created_at: string;
}

export interface InterviewSessionDetail {
  id: string;
  status: 'in_progress' | 'completed' | 'abandoned';
  config: Record<string, any>;
  adaptive_state: Record<string, any>;
  started_at?: string | null;
  ended_at?: string | null;
  final_score?: number | null;
  report?: Record<string, any> | null;
  turns: InterviewTurn[];
  created_at: string;
}

export interface InterviewReport {
  session_id: string;
  status: string;
  final_score: number;
  performance_band: string;
  total_questions: number;
  dimension_breakdown: Array<{
    dimension: string;
    average_mark: number;
    percentage: number;
  }>;
  strengths: string[];
  areas_for_improvement: string[];
  practice_recommendations: string[];
  turns: InterviewTurn[];
}

export const interviewsApi = {
  createSession: async (data: {
    target_role?: string;
    company?: string;
    interview_stage?: string;
    difficulty?: string;
    duration_minutes?: number;
    num_questions?: number;
    mode?: string;
    preset?: string;
  }) => {
    const res = await apiClient.post<InterviewSessionDetail>('/interviews/sessions', data);
    return res.data;
  },

  listSessions: async (limit = 20) => {
    const res = await apiClient.get<InterviewSessionSummary[]>('/interviews/sessions', {
      params: { limit },
    });
    return res.data;
  },

  getSession: async (sessionId: string) => {
    const res = await apiClient.get<InterviewSessionDetail>(`/interviews/sessions/${sessionId}`);
    return res.data;
  },

  submitAnswer: async (sessionId: string, answerText: string) => {
    const res = await apiClient.post<InterviewSessionDetail>(
      `/interviews/sessions/${sessionId}/answer`,
      { answer_text: answerText }
    );
    return res.data;
  },

  retryTurn: async (sessionId: string, turnId: string) => {
    const res = await apiClient.post<InterviewTurn>(
      `/interviews/sessions/${sessionId}/retry-eval/${turnId}`
    );
    return res.data;
  },

  finishEarly: async (sessionId: string) => {
    const res = await apiClient.post<InterviewSessionDetail>(
      `/interviews/sessions/${sessionId}/finish`
    );
    return res.data;
  },

  getReport: async (sessionId: string) => {
    const res = await apiClient.get<InterviewReport>(`/interviews/sessions/${sessionId}/report`);
    return res.data;
  },
};
