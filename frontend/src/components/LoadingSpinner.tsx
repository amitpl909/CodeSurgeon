import React from 'react';

export const LoadingSpinner: React.FC<{ message?: string }> = ({ message = 'Processing...' }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="animate-spin rounded-full h-12 w-12 border-4 border-gray-300 border-t-blue-600 mb-4"></div>
      <p className="text-gray-600">{message}</p>
    </div>
  );
};
