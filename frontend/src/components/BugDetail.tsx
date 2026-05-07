import React, { useEffect, useState } from 'react';
import { Bug } from '../store/analysisStore';
import { generateFixes } from '../services/api';

interface BugDetailProps {
  bug: Bug;
  analysisId: string;
}

export const BugDetail: React.FC<BugDetailProps> = ({ bug, analysisId }) => {
  const [loadingFix, setLoadingFix] = useState(false);
  const [fix, setFix] = useState(bug.fix);
  const [alternatives, setAlternatives] = useState(bug.alternatives);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateFixes = async () => {
    try {
      setLoadingFix(true);
      setError(null);
      const response = await generateFixes(bug.id, analysisId);
      setFix(response.fix);
      setAlternatives(response.alternatives);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate fixes');
    } finally {
      setLoadingFix(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-bold mb-4">{bug.description}</h3>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div>
          <p className="text-sm text-gray-600">Type</p>
          <p className="font-semibold capitalize">{bug.type.replace(/_/g, ' ')}</p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Severity</p>
          <p className="font-semibold">{bug.severity}</p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Line Number</p>
          <p className="font-semibold">{bug.line}</p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Confidence</p>
          <p className="font-semibold">{(bug.confidence * 100).toFixed(0)}%</p>
        </div>
      </div>

      <div className="mb-6">
        <h4 className="font-semibold mb-2">Code Snippet</h4>
        <pre className="bg-red-50 border border-red-200 rounded p-3 text-sm font-mono overflow-x-auto">
          {bug.code_snippet}
        </pre>
      </div>

      <div className="mb-6">
        <h4 className="font-semibold mb-2">Explanation</h4>
        <p className="text-gray-700">{bug.explanation}</p>
      </div>

      {fix && (
        <div className="mb-6 bg-green-50 border border-green-200 rounded p-4">
          <div className="flex justify-between items-center mb-2">
            <h4 className="font-semibold">Suggested Fix</h4>
            <button
              onClick={() => copyToClipboard(fix.corrected_code)}
              className="text-sm px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
            >
              Copy
            </button>
          </div>
          <pre className="bg-white border border-green-200 rounded p-3 text-sm font-mono overflow-x-auto mb-2">
            {fix.corrected_code}
          </pre>
          <p className="text-sm text-gray-600">{fix.explanation}</p>
        </div>
      )}

      {alternatives && alternatives.length > 0 && (
        <div className="mb-6">
          <h4 className="font-semibold mb-2">Alternative Solutions</h4>
          <div className="space-y-3">
            {alternatives.map((alt, idx) => (
              <div key={idx} className="bg-blue-50 border border-blue-200 rounded p-3">
                <div className="flex justify-between items-center mb-2">
                  <p className="text-sm font-semibold">{alt.note}</p>
                  <button
                    onClick={() => copyToClipboard(alt.code)}
                    className="text-xs px-2 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
                  >
                    Copy
                  </button>
                </div>
                <pre className="bg-white border border-blue-200 rounded p-2 text-xs font-mono overflow-x-auto">
                  {alt.code}
                </pre>
              </div>
            ))}
          </div>
        </div>
      )}

      {!fix && (
        <div>
          <button
            onClick={handleGenerateFixes}
            disabled={loadingFix}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loadingFix ? 'Generating...' : 'Generate Fixes'}
          </button>
          {error && <p className="text-red-600 text-sm mt-2">{error}</p>}
        </div>
      )}
    </div>
  );
};
