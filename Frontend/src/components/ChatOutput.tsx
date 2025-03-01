import React from 'react';
import ReactMarkdown from 'react-markdown';

interface ChatOutputProps {
  messages: Array<{
    text: string;
    type: 'system';
  }>;
}

const ChatOutput: React.FC<ChatOutputProps> = ({ messages }) => {
  const message = messages[0];

  return (
    <div className="bg-gray-50 p-4 h-64 overflow-y-auto border border-gray-200 rounded-lg">
      {message ? (
        <ReactMarkdown>{message.text}</ReactMarkdown>
      ) : (
        <div className="text-gray-400 text-center flex items-center justify-center h-full">
          <p>No analysis data yet. Search for a company to begin.</p>
        </div>
      )}
    </div>
  );
};

export default ChatOutput;
