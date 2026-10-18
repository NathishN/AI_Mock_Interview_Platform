import { apiClient } from './client';

export interface AnalyticsOverview {
  total_sessions: number;
  completed_sessions: number;
  total_questions_answered: number;
  average_score: number;
  readiness_score: number;
  current_streak_days: number;
  performance_band: string;
}

export interface SkillScore {
  category: string;
  score: number;
  total_evaluated: number;
}

export interface ScoreHistoryPoint {
  session_id: string;
  date: string;
  role: string;
  score: number;
}

export interface WeakAreaItem {
  topic: string;
  category: string;
  frequency: number;
  average_score: number;
  recommendation: string;
}

export const analyticsApi = {
  getOverview: async () => {
    const res = await apiClient.get<AnalyticsOverview>('/analytics/overview');
    return res.data;
  },

  getSkills: async () => {
    const res = await apiClient.get<SkillScore[]>('/analytics/skills');
    return res.data;
  },

  getHistory: async () => {
    const res = await apiClient.get<ScoreHistoryPoint[]>('/analytics/history');
    return res.data;
  },

  getWeaknesses: async () => {
    const res = await apiClient.get<WeakAreaItem[]>('/analytics/weaknesses');
    return res.data;
  },
};
