import React from 'react';

interface ChatOutputProps {
  messages: Array<{
    text: string;
    type: 'system' | 'analysis';
  }>;
}

const ChatOutput: React.FC<ChatOutputProps> = ({ messages }) => {
  return (
    <div className="bg-gray-50 rounded-lg p-4 h-64 overflow-y-auto border border-gray-200">
      {messages.length === 0 ? (
        <div className="text-gray-400 text-center h-full flex items-center justify-center">
          <p>No analysis data yet. Search for a company to begin.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {messages.map((message, index) => (
            <div 
              key={index} 
              className={`p-3 rounded-lg ${
                message.type === 'system' 
                  ? 'bg-gray-100 text-gray-700' 
                  : 'bg-indigo-100 text-indigo-700 font-medium'
              }`}
            >
              {message.text}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ChatOutput;