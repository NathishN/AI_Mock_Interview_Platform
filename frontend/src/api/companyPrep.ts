import { apiClient } from './client';

export interface CompanyRound {
  round_number: number;
  name: string;
  stage: string;
  duration_minutes: number;
  description: string;
  focus_areas: string[];
}

export interface CompanyGuide {
  id: string;
  name: string;
  slug: string;
  logo_letter: string;
  category: string;
  difficulty: string;
  hiring_rounds: number;
  description: string;
  rounds: CompanyRound[];
  key_tips: string[];
  recommended_question_categories: string[];
}

export const companyPrepApi = {
  listCompanies: async () => {
    const res = await apiClient.get<CompanyGuide[]>('/company-prep');
    return res.data;
  },

  getCompanyDetail: async (slug: string) => {
    const res = await apiClient.get<CompanyGuide>(`/company-prep/${slug}`);
    return res.data;
  },
};
