import { apiClient } from './client';

export interface HRTopicField {
  key: string;
  label: string;
  placeholder: string;
}

export interface HRTopic {
  id: string;
  title: string;
  framework: string;
  description: string;
  prompt_fields: HRTopicField[];
}

export interface HRAnalysisResult {
  score: number;
  strengths: string[];
  vague_phrases: string[];
  unsupported_claims: string[];
  structure_feedback: string;
  coaching_tips: string[];
}

export interface HRDraft {
  id: string;
  topic: string;
  facts: Record<string, any>;
  generated_answer?: string | null;
  final_answer?: string | null;
  created_at: string;
  updated_at: string;
}

export const hrStudioApi = {
  getTopics: async () => {
    const res = await apiClient.get<HRTopic[]>('/hr-studio/topics');
    return res.data;
  },

  generateAnswer: async (topic: string, facts: Record<string, any>) => {
    const res = await apiClient.post<{ topic: string; generated_answer: string }>(
      '/hr-studio/generate',
      { topic, facts }
    );
    return res.data;
  },

  analyzeDraft: async (topic: string, answerText: string) => {
    const res = await apiClient.post<HRAnalysisResult>('/hr-studio/analyze', {
      topic,
      answer_text: answerText,
    });
    return res.data;
  },

  listDrafts: async () => {
    const res = await apiClient.get<HRDraft[]>('/hr-studio/drafts');
    return res.data;
  },

  saveDraft: async (data: {
    topic: string;
    facts: Record<string, any>;
    generated_answer?: string | null;
    final_answer: string;
  }) => {
    const res = await apiClient.post<HRDraft>('/hr-studio/drafts', data);
    return res.data;
  },

  deleteDraft: async (draftId: string) => {
    await apiClient.delete(`/hr-studio/drafts/${draftId}`);
  },
};
