import React from 'react';
import { Bug } from '../store/analysisStore';

interface BugsListProps {
  bugs: Bug[];
  selectedBugId: string | null;
  onSelectBug: (bugId: string) => void;
}

const getSeverityColor = (severity: string) => {
  switch (severity) {
    case 'CRITICAL':
      return 'bg-red-100 border-red-300 text-red-900';
    case 'HIGH':
      return 'bg-orange-100 border-orange-300 text-orange-900';
    case 'MEDIUM':
      return 'bg-yellow-100 border-yellow-300 text-yellow-900';
    case 'LOW':
      return 'bg-green-100 border-green-300 text-green-900';
    default:
      return 'bg-gray-100 border-gray-300 text-gray-900';
  }
};

const getSeverityBadge = (severity: string) => {
  switch (severity) {
    case 'CRITICAL':
      return '🔴';
    case 'HIGH':
      return '🟠';
    case 'MEDIUM':
      return '🟡';
    case 'LOW':
      return '🟢';
    default:
      return '⚪';
  }
};

export const BugsList: React.FC<BugsListProps> = ({ bugs, selectedBugId, onSelectBug }) => {
  if (bugs.length === 0) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
        <p className="text-green-700 font-semibold">✓ No bugs detected!</p>
        <p className="text-green-600 text-sm mt-1">Your code looks clean.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {bugs.map((bug) => (
        <button
          key={bug.id}
          onClick={() => onSelectBug(bug.id)}
          className={`w-full text-left p-4 border-2 rounded-lg transition-all ${
            selectedBugId === bug.id
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-200 hover:border-gray-300'
          } ${getSeverityColor(bug.severity)}`}
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-lg">{getSeverityBadge(bug.severity)}</span>
                <span className="font-semibold">{bug.description}</span>
                <span className="text-xs px-2 py-1 bg-white rounded opacity-70">
                  Line {bug.line}
                </span>
              </div>
              <p className="text-sm opacity-75 mt-1 font-mono">{bug.code_snippet.substring(0, 60)}...</p>
            </div>
            <div className="ml-4 text-right">
              <div className="text-xs px-2 py-1 bg-white rounded opacity-70">
                {(bug.confidence * 100).toFixed(0)}% sure
              </div>
            </div>
          </div>
        </button>
      ))}
    </div>
  );
};
