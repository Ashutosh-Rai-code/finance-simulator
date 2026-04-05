import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error?.response?.data?.detail || error?.message || 'Unknown error';
    return Promise.reject(new Error(message));
  }
);

export interface FinancialInput {
  income: number;
  expenses: number;
  savings: number;
  sip: number;
  target_goal: number;
}

export interface Metrics {
  savings_rate: number;
  emergency_months: number;
  sip_ratio: number;
  monthly_surplus: number;
  goal_progress: number;
}

export interface Risk {
  risk: string;
  recommendation: string;
  severity: 'low' | 'medium' | 'high';
}

export const financialService = {
  calculateMetrics: (data: FinancialInput) =>
    api.post<Metrics>('/financial/metrics', data),
  
  analyzeRisks: (data: FinancialInput) =>
    api.post('/financial/risks', data),
  
  getRoadmap: (data: FinancialInput) =>
    api.post('/financial/roadmap', data),
  
  getGoalProgress: (data: FinancialInput) =>
    api.post('/financial/goal-progress', data),
  
  whatIfSimulation: (data: FinancialInput, newSip: number, rateOfReturn: number, durationYears: number) =>
    api.post('/financial/what-if', {
      ...data,
      new_sip: newSip,
      rate_of_return: rateOfReturn / 100,
      duration_years: durationYears,
    }),
};

export const aiService = {
  getAdvice: (data: FinancialInput) =>
    api.post('/ai/advice', { ...data, execute_ai: true }, { timeout: 60000 }),
  
  analyzeQuitJob: (savings: number, expenses: number) =>
    api.post('/ai/quit-job-analysis', { savings, expenses, execute_ai: true }, { timeout: 60000 }),
};

export const visitorService = {
  getVisitorCount: () => api.get<{ count: number }>('/visitors'),
  incrementVisitorCount: () => api.post<{ count: number }>('/visitors'),
};

export default api;
