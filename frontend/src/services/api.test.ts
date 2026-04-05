import axios from 'axios';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

// Mock the api module with implementations that call axios
jest.mock('../services/api', () => ({
  financialService: {
    calculateMetrics: jest.fn(async (data) => {
      const response = await mockedAxios.post('/financial/metrics', data);
      return response.data;
    }),
    analyzeRisks: jest.fn(async (data) => {
      const response = await mockedAxios.post('/financial/risks', data);
      return response.data;
    }),
    getRoadmap: jest.fn(async (data) => {
      const response = await mockedAxios.post('/financial/roadmap', data);
      return response.data;
    }),
    whatIfSimulation: jest.fn(async (data, newSip) => {
      const response = await mockedAxios.post('/financial/what-if', { ...data, new_sip: newSip });
      return response.data;
    }),
  },
  aiService: {
    getAdvice: jest.fn(async (data) => {
      const response = await mockedAxios.post('/ai/advice', { ...data, execute_ai: true });
      return response.data;
    }),
    analyzeQuitJob: jest.fn(async (savings, expenses) => {
      const response = await mockedAxios.post('/ai/quit-job-analysis', { savings, expenses, execute_ai: true });
      return response.data;
    }),
  },
  visitorService: {
    getVisitorCount: jest.fn(async () => {
      const response = await mockedAxios.get('/visitors');
      return response.data;
    }),
    incrementVisitorCount: jest.fn(async () => {
      const response = await mockedAxios.post('/visitors');
      return response.data;
    }),
  },
}));

import { financialService, aiService, visitorService } from '../services/api';

describe('API Services', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Financial Service', () => {
    test('calculateMetrics calls correct endpoint', async () => {
      const mockData = {
        income: 100000,
        expenses: 50000,
        savings: 200000,
        sip: 10000,
        target_goal: 1000000
      };
      const mockResponse = {
        savings_rate: 50,
        emergency_months: 4,
        sip_ratio: 10,
        monthly_surplus: 50000,
        goal_progress: 20
      };

      mockedAxios.post.mockResolvedValueOnce({ data: mockResponse });

      const result = await financialService.calculateMetrics(mockData);

      expect(mockedAxios.post).toHaveBeenCalledWith('/financial/metrics', mockData);
      expect(result).toEqual(mockResponse);
    });

    test('analyzeRisks calls correct endpoint', async () => {
      const mockData = {
        income: 100000,
        expenses: 50000,
        savings: 200000,
        sip: 10000,
        target_goal: 1000000
      };
      const mockResponse = { risks: [] };

      mockedAxios.post.mockResolvedValueOnce({ data: mockResponse });

      const result = await financialService.analyzeRisks(mockData);

      expect(mockedAxios.post).toHaveBeenCalledWith('/financial/risks', mockData);
      expect(result).toEqual(mockResponse);
    });

    test('whatIfSimulation calls correct endpoint', async () => {
      const mockData = {
        income: 100000,
        expenses: 50000,
        savings: 200000,
        sip: 10000,
        target_goal: 1000000
      };
      const newSip = 15000;
      const rateOfReturn = 12;
      const durationYears = 10;
      const mockResponse = {
        current_roadmap: [],
        new_roadmap: [],
        additional_wealth: 100000
      };

      mockedAxios.post.mockResolvedValueOnce({ data: mockResponse });

      const result = await financialService.whatIfSimulation(mockData, newSip, rateOfReturn, durationYears);

      expect(mockedAxios.post).toHaveBeenCalledWith('/financial/what-if', {
        ...mockData,
        new_sip: newSip,
        rate_of_return: rateOfReturn / 100,
        duration_years: durationYears,
      });
      expect(result).toEqual(mockResponse);
    });
  });

  describe('AI Service', () => {
    test('getAdvice calls correct endpoint', async () => {
      const mockData = {
        income: 100000,
        expenses: 50000,
        savings: 200000,
        sip: 10000
      };
      const mockResponse = {
        immediate_actions: ['Action 1'],
        ninety_day_plan: ['Plan 1'],
        one_year_vision: 'Vision'
      };

      mockedAxios.post.mockResolvedValueOnce({ data: mockResponse });

      const result = await aiService.getAdvice(mockData);

      expect(mockedAxios.post).toHaveBeenCalledWith('/ai/advice', { ...mockData, execute_ai: true });
      expect(result).toEqual(mockResponse);
    });

    test('analyzeQuitJob calls correct endpoint', async () => {
      const savings = 200000;
      const expenses = 50000;
      const mockResponse = {
        survival_months: 4,
        risk_level: 'medium',
        advice: 'Advice text'
      };

      mockedAxios.post.mockResolvedValueOnce({ data: mockResponse });

      const result = await aiService.analyzeQuitJob(savings, expenses);

      expect(mockedAxios.post).toHaveBeenCalledWith('/ai/quit-job-analysis', {
        savings,
        expenses,
        execute_ai: true
      });
      expect(result).toEqual(mockResponse);
    });
  });

  describe('Visitor Service', () => {
    test('incrementVisitorCount calls correct endpoint', async () => {
      const mockResponse = { count: 123 };
      mockedAxios.post.mockResolvedValueOnce({ data: mockResponse });

      const result = await visitorService.incrementVisitorCount();

      expect(mockedAxios.post).toHaveBeenCalledWith('/visitors');
      expect(result).toEqual(mockResponse);
    });

    test('getVisitorCount calls correct endpoint', async () => {
      const mockResponse = { count: 456 };
      mockedAxios.get.mockResolvedValueOnce({ data: mockResponse });

      const result = await visitorService.getVisitorCount();

      expect(mockedAxios.get).toHaveBeenCalledWith('/visitors');
      expect(result).toEqual(mockResponse);
    });
  });
});