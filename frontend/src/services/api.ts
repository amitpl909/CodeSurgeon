import axios, { AxiosError } from 'axios';
import { AnalysisResult, Bug } from '../store/analysisStore';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzeCode = async (
  input: string,
  type: 'pr' | 'snippet',
  language: string = 'auto',
  context?: Record<string, string>
): Promise<AnalysisResult> => {
  try {
    const response = await apiClient.post<AnalysisResult>('/api/v1/analyze', {
      type,
      input,
      language,
      context,
    });
    return response.data;
  } catch (error) {
    const axiosError = error as AxiosError;
    throw new Error(
      axiosError.response?.data?.detail ||
      'Failed to analyze code'
    );
  }
};

export const getAnalysis = async (analysisId: string): Promise<AnalysisResult> => {
  try {
    const response = await apiClient.get<AnalysisResult>(
      `/api/v1/analysis/${analysisId}`
    );
    return response.data;
  } catch (error) {
    throw new Error('Failed to retrieve analysis');
  }
};

export const generateFixes = async (
  bugId: string,
  analysisId: string
): Promise<{
  bug_id: string;
  fix: { corrected_code: string; explanation: string; confidence: number };
  alternatives?: Array<{ code: string; note: string }>;
}> => {
  try {
    const response = await apiClient.post('/api/v1/fixes', {
      bug_id: bugId,
      analysis_id: analysisId,
    });
    return response.data;
  } catch (error) {
    throw new Error('Failed to generate fixes');
  }
};

export const checkHealth = async (): Promise<{
  status: string;
  services: Record<string, string>;
}> => {
  try {
    const response = await apiClient.get('/api/v1/health');
    return response.data;
  } catch (error) {
    throw new Error('Health check failed');
  }
};
