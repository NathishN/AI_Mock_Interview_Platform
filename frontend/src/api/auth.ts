import { apiClient } from './client';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'user' | 'admin';
  is_active: boolean;
}

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface AuthResponse {
  user: User;
  tokens: TokenPair;
}

export const authApi = {
  register: async (data: { email: string; password: string; full_name: string }) => {
    const res = await apiClient.post<AuthResponse>('/auth/register', data);
    return res.data;
  },

  login: async (data: { email: string; password: string }) => {
    const res = await apiClient.post<AuthResponse>('/auth/login', data);
    return res.data;
  },

  getMe: async () => {
    const res = await apiClient.get<User>('/auth/me');
    return res.data;
  },

  resetPassword: async (data: { email: string; new_password: string }) => {
    const res = await apiClient.post<{ message: string }>('/auth/reset-password', data);
    return res.data;
  },
};
