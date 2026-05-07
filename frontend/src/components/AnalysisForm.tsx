import React, { useState } from 'react';

interface AnalysisFormProps {
  onAnalyze: (
    input: string,
    type: 'pr' | 'snippet',
    language: string
  ) => Promise<void>;
  loading?: boolean;
}

export const AnalysisForm: React.FC<AnalysisFormProps> = ({ onAnalyze, loading = false }) => {
  const [input, setInput] = useState('');
  const [type, setType] = useState<'pr' | 'snippet'>('snippet');
  const [language, setLanguage] = useState('auto');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!input.trim()) {
      setError('Please enter code or PR URL');
      return;
    }

    try {
      await onAnalyze(input, type, language);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4">CodeSurgeon</h2>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">Analysis Type</label>
        <div className="flex gap-4">
          <label className="flex items-center">
            <input
              type="radio"
              value="snippet"
              checked={type === 'snippet'}
              onChange={(e) => setType(e.target.value as 'snippet')}
              className="mr-2"
            />
            Code Snippet
          </label>
          <label className="flex items-center">
            <input
              type="radio"
              value="pr"
              checked={type === 'pr'}
              onChange={(e) => setType(e.target.value as 'pr')}
              className="mr-2"
            />
            GitHub PR URL
          </label>
        </div>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">Language</label>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
        >
          <option value="auto">Auto-detect</option>
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="typescript">TypeScript</option>
          <option value="java">Java</option>
          <option value="go">Go</option>
        </select>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">
          {type === 'pr' ? 'GitHub PR URL' : 'Code Snippet'}
        </label>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={
            type === 'pr'
              ? 'https://github.com/user/repo/pull/123'
              : 'Paste your code here...'
          }
          rows={10}
          className="w-full px-3 py-2 border border-gray-300 rounded-md font-mono text-sm"
          disabled={loading}
        />
      </div>

      {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">{error}</div>}

      <div className="flex gap-2">
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
        <button
          type="button"
          onClick={() => setInput('')}
          disabled={loading}
          className="px-6 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 disabled:bg-gray-100"
        >
          Clear
        </button>
      </div>
    </form>
  );
};
