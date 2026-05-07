import React from 'react';
import { AnalysisResult } from '../store/analysisStore';

interface ResultsSummaryProps {
  analysis: AnalysisResult;
}

export const ResultsSummary: React.FC<ResultsSummaryProps> = ({ analysis }) => {
  const { summary } = analysis;

  return (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4">Analysis Results</h2>

      <div className="grid grid-cols-5 gap-4">
        <div className="bg-white rounded p-4 text-center">
          <p className="text-3xl font-bold text-blue-600">{summary.total_bugs}</p>
          <p className="text-sm text-gray-600">Total Bugs</p>
        </div>

        <div className="bg-white rounded p-4 text-center">
          <p className="text-3xl font-bold text-red-600">{summary.critical}</p>
          <p className="text-sm text-gray-600">Critical</p>
        </div>

        <div className="bg-white rounded p-4 text-center">
          <p className="text-3xl font-bold text-orange-600">{summary.high}</p>
          <p className="text-sm text-gray-600">High</p>
        </div>

        <div className="bg-white rounded p-4 text-center">
          <p className="text-3xl font-bold text-yellow-600">{summary.medium}</p>
          <p className="text-sm text-gray-600">Medium</p>
        </div>

        <div className="bg-white rounded p-4 text-center">
          <p className="text-3xl font-bold text-green-600">{summary.low}</p>
          <p className="text-sm text-gray-600">Low</p>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-blue-200">
        <p className="text-sm text-gray-600">
          Analysis completed in <span className="font-semibold">{summary.analysis_time_ms}ms</span>
        </p>
      </div>
    </div>
  );
};
