import { apiClient } from './client';

export interface UserProfile {
  id: string;
  degree?: string;
  branch?: string;
  graduation_year?: number;
  target_role?: string;
  preferred_companies: string[];
  interview_experience?: string;
  weakness_areas: string[];
  preferred_language: string;
  daily_prep_minutes: number;
  interview_goals?: string;
  updated_at: string;
}

export const profileApi = {
  getProfile: async () => {
    const res = await apiClient.get<UserProfile>('/profile');
    return res.data;
  },

  updateProfile: async (data: Partial<UserProfile>) => {
    const res = await apiClient.put<UserProfile>('/profile', data);
    return res.data;
  },
};
