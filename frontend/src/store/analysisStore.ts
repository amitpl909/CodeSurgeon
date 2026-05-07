import { create } from 'zustand';

export interface Bug {
  id: string;
  type: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  line: number;
  code_snippet: string;
  description: string;
  explanation: string;
  confidence: number;
  fix?: {
    corrected_code: string;
    explanation: string;
    confidence: number;
  };
  alternatives?: Array<{
    code: string;
    note: string;
  }>;
}

export interface AnalysisSummary {
  total_bugs: number;
  critical: number;
  high: number;
  medium: number;
  low: number;
  analysis_time_ms: number;
}

export interface AnalysisResult {
  id: string;
  status: string;
  timestamp: string;
  bugs: Bug[];
  summary: AnalysisSummary;
  error?: string;
}

interface AnalysisStore {
  analysis: AnalysisResult | null;
  selectedBugId: string | null;
  loading: boolean;
  error: string | null;
  
  setAnalysis: (analysis: AnalysisResult | null) => void;
  setSelectedBugId: (bugId: string | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearAnalysis: () => void;
  
  selectedBug: () => Bug | undefined;
}

export const useAnalysisStore = create<AnalysisStore>((set, get) => ({
  analysis: null,
  selectedBugId: null,
  loading: false,
  error: null,

  setAnalysis: (analysis) => set({ analysis }),
  setSelectedBugId: (bugId) => set({ selectedBugId: bugId }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  clearAnalysis: () => set({ analysis: null, selectedBugId: null, error: null }),

  selectedBug: () => {
    const { analysis, selectedBugId } = get();
    if (!analysis || !selectedBugId) return undefined;
    return analysis.bugs.find((bug) => bug.id === selectedBugId);
  },
}));
