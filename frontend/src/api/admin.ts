import { apiClient } from './client';
import { Question } from './questions';

export const adminApi = {
  createQuestion: async (data: Partial<Question>) => {
    const res = await apiClient.post<Question>('/admin/questions', data);
    return res.data;
  },

  updateQuestion: async (id: string, data: Partial<Question>) => {
    const res = await apiClient.put<Question>(`/admin/questions/${id}`, data);
    return res.data;
  },

  deleteQuestion: async (id: string) => {
    await apiClient.delete(`/admin/questions/${id}`);
  },
};
