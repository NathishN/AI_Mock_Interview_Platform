import { apiClient } from './client';

export interface Milestone {
  week: number;
  title: string;
  focus: string;
  estimated_hours: number;
  topics: string[];
  practice_actions: string[];
  completed: boolean;
}

export interface LearningRoadmap {
  target_role: string;
  target_companies: string[];
  total_weeks: number;
  readiness_level: string;
  milestones: Milestone[];
}

export const roadmapApi = {
  getRoadmap: async () => {
    const res = await apiClient.get<LearningRoadmap>('/roadmap');
    return res.data;
  },
};
