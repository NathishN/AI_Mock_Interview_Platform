import { apiClient } from './client';
import { InterviewSessionDetail } from './interviews';

export interface ResumeQuestion {
  id: string;
  question: string;
  category: string;
  topic: string;
  difficulty: string;
  rubric_key: string;
  interviewer_context?: string | null;
  key_points: string[];
  ideal_answer_outline?: string | null;
}

export interface ResumeAnalysis {
  overview_summary: string;
  ats_score: number;
  ats_breakdown: {
    skill_relevance?: number;
    project_depth?: number;
    impact_metrics?: number;
    formatting_structure?: number;
    [key: string]: number | undefined;
  };
  strengths: string[];
  flagged_risks: string[];
  recommended_focus_areas: string[];
  generated_questions: ResumeQuestion[];
}

export interface ResumeParsedData {
  candidate_name?: string;
  skills: {
    languages?: string[];
    frameworks_and_libraries?: string[];
    databases?: string[];
    tools_and_platforms?: string[];
    core_competencies?: string[];
    [key: string]: string[] | undefined;
  };
  projects: Array<{
    title: string;
    technologies?: string[];
    summary?: string;
    claimed_impact?: string;
  }>;
  experience: Array<{
    role: string;
    company: string;
    duration?: string;
    summary?: string;
  }>;
  education: Array<{
    degree: string;
    institution?: string;
    graduation_year?: string | number;
    gpa_or_percentage?: string;
  }>;
}

export interface ResumeDetail {
  id: string;
  filename: string;
  file_type: string;
  file_size_bytes: number;
  raw_text: string;
  target_role?: string;
  parsed_data: ResumeParsedData;
  analysis: ResumeAnalysis;
  is_active: boolean;
  created_at: string;
}

export interface ResumeSummary {
  id: string;
  filename: string;
  file_type: string;
  file_size_bytes: number;
  target_role?: string;
  ats_score?: number | null;
  created_at: string;
}

export const resumesApi = {
  uploadFile: async (file: File, targetRole: string = 'Software Development Engineer'): Promise<ResumeDetail> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('target_role', targetRole);
    const res = await apiClient.post<ResumeDetail>('/resumes/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },

  uploadText: async (rawText: string, targetRole: string = 'Software Development Engineer'): Promise<ResumeDetail> => {
    const res = await apiClient.post<ResumeDetail>('/resumes/upload-text', {
      raw_text: rawText,
      target_role: targetRole,
    });
    return res.data;
  },

  getLatest: async (): Promise<ResumeDetail> => {
    const res = await apiClient.get<ResumeDetail>('/resumes/latest');
    return res.data;
  },

  list: async (): Promise<ResumeSummary[]> => {
    const res = await apiClient.get<ResumeSummary[]>('/resumes');
    return res.data;
  },

  getById: async (id: string): Promise<ResumeDetail> => {
    const res = await apiClient.get<ResumeDetail>(`/resumes/${id}`);
    return res.data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/resumes/${id}`);
  },

  startInterview: async (
    resumeId: string,
    config: { num_questions?: number; target_role?: string; company?: string } = {}
  ): Promise<InterviewSessionDetail> => {
    const res = await apiClient.post<InterviewSessionDetail>(`/resumes/${resumeId}/start-interview`, config);
    return res.data;
  },

  evaluateQuestion: async (
    resumeId: string,
    data: {
      question_id: string;
      question_text: string;
      answer_text: string;
      target_role?: string;
      rubric_key?: string;
    }
  ): Promise<any> => {
    const res = await apiClient.post<any>(`/resumes/${resumeId}/evaluate-question`, data);
    return res.data;
  },
};
