import { apiClient } from './client';

export interface Question {
  id: string;
  category: string;
  subcategory?: string;
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  question: string;
  target_roles: string[];
  interview_stage: string[];
  reference_answer: string;
  key_points: string[];
  evaluation_criteria: string[];
  common_mistakes: string[];
  follow_up_questions: string[];
  tags: string[];
  is_active: boolean;
}

export interface QuestionListResponse {
  total: number;
  items: Question[];
}

export const questionsApi = {
  list: async (params?: {
    category?: string;
    difficulty?: string;
    role?: string;
    stage?: string;
    tag?: string;
    search?: string;
    limit?: number;
    offset?: number;
  }) => {
    const res = await apiClient.get<QuestionListResponse>('/questions', { params });
    return res.data;
  },

  getById: async (id: string) => {
    const res = await apiClient.get<Question>(`/questions/${id}`);
    return res.data;
  },
};
