import React, { useState } from 'react';
import { analyzeCode } from '../services/api';
import { useAnalysisStore } from '../store/analysisStore';
import { AnalysisForm } from './AnalysisForm';
import { ResultsSummary } from './ResultsSummary';
import { BugsList } from './BugsList';
import { BugDetail } from './BugDetail';
import { LoadingSpinner } from './LoadingSpinner';

export const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const {
    analysis,
    selectedBugId,
    setAnalysis,
    setSelectedBugId,
    setError,
    error,
  } = useAnalysisStore();

  const handleAnalyze = async (
    input: string,
    type: 'pr' | 'snippet',
    language: string
  ) => {
    setLoading(true);
    setError(null);

    try {
      const result = await analyzeCode(input, type, language);
      setAnalysis(result);
      setSelectedBugId(result.bugs.length > 0 ? result.bugs[0].id : null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900">CodeSurgeon</h1>
          <p className="text-gray-600 mt-2">
            AI-powered bug detection and repair agent for GitHub
          </p>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Form */}
          <div className="lg:col-span-1">
            <AnalysisForm onAnalyze={handleAnalyze} loading={loading} />
          </div>

          {/* Right Column - Results */}
          <div className="lg:col-span-2">
            {loading && <LoadingSpinner message="Analyzing your code..." />}

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                <p className="text-red-700">{error}</p>
              </div>
            )}

            {analysis && !loading && (
              <>
                <ResultsSummary analysis={analysis} />

                <div className="grid grid-cols-1 gap-6">
                  {/* Bugs List */}
                  <div>
                    <h3 className="text-xl font-bold mb-4">Detected Issues</h3>
                    <BugsList
                      bugs={analysis.bugs}
                      selectedBugId={selectedBugId}
                      onSelectBug={setSelectedBugId}
                    />
                  </div>

                  {/* Bug Detail */}
                  {selectedBugId && (
                    <div>
                      <h3 className="text-xl font-bold mb-4">Details & Fixes</h3>
                      {analysis.bugs
                        .filter((bug) => bug.id === selectedBugId)
                        .map((bug) => (
                          <BugDetail key={bug.id} bug={bug} analysisId={analysis.id} />
                        ))}
                    </div>
                  )}
                </div>
              </>
            )}

            {!analysis && !loading && !error && (
              <div className="text-center py-12">
                <p className="text-gray-500">
                  Submit code to get started with bug analysis
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
