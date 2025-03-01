import React from 'react';
import ReactMarkdown from 'react-markdown';

interface InvestmentSummaryProps {
  company: string;
  sentiment: 'bullish' | 'bearish' | 'neutral';
  recommendation: {
    "Financial Health": string;
    "Market Sentiment": string;
    "Recommendation": string;
  };
}

const InvestmentSummary: React.FC<InvestmentSummaryProps> = ({ company, sentiment, recommendation }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {/* Financial Health */}
      <div className="bg-white rounded-lg shadow-md border-t-4 border-blue-500 h-96">
        <div className="p-6 flex flex-col h-full">
          <h3 className="text-lg font-medium mb-4 text-blue-700">
            Financial Health
          </h3>
          <div className="text-sm text-gray-600 overflow-y-auto scrollbar-hide">
            <ReactMarkdown>
              {recommendation["Financial Health"]}
            </ReactMarkdown>
          </div>
        </div>
      </div>
      
      {/* Market Sentiment */}
      <div className="bg-white rounded-lg shadow-md border-t-4 border-purple-500 h-96">
        <div className="p-6 flex flex-col h-full">
          <h3 className="text-lg font-medium mb-4 text-purple-700">
            Market Sentiment
          </h3>
          <div className="text-sm text-gray-600 overflow-y-auto scrollbar-hide">
            <ReactMarkdown>
              {recommendation["Market Sentiment"]}
            </ReactMarkdown>
          </div>
        </div>
      </div>
      
      {/* Recommendation */}
      <div className={`bg-white rounded-lg shadow-md border-t-4 
        ${sentiment === 'bullish' ? 'border-green-500' : 
          sentiment === 'bearish' ? 'border-red-500' : 'border-yellow-500'} h-96`}>
        <div className="p-6 flex flex-col h-full">
          <h3 className={`text-lg font-medium mb-4 
            ${sentiment === 'bullish' ? 'text-green-700' : 
              sentiment === 'bearish' ? 'text-red-700' : 'text-yellow-700'}`}>
            Recommendation
          </h3>
          <div className="text-sm text-gray-600 overflow-y-auto scrollbar-hide">
            <ReactMarkdown>
              {recommendation["Recommendation"]}
            </ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InvestmentSummary;
